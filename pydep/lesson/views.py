import calendar
import uuid
from datetime import datetime
from urllib.parse import urlencode
from urllib.parse import unquote

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .forms import EditProfile
from .models import Course
from .models import Module
from .models import Lesson
from .models import Category
from .models import UserLessonProgress
from users.models import CancelledLesson
from users.models import Schedule
from .paginator import paginator


def query_params_in_dict(query_params: str) -> dict:
    query_params = query_params.replace("&", " ").replace("=", " ").split()
    return {
        query_params[i]: query_params[i + 1]
        for i in range(0, len(query_params) - 1, 2)
    } if query_params else {}


def search_course_with_name(
        name: str,
        base_queryset: QuerySet = None
) -> QuerySet:
    """
    Поиск курса по имени (регистронезависимо) с использованием Python.
    Работает с существующим QuerySet.
    """
    name = unquote(name).strip()
    if not name:
        return base_queryset or Course.objects.filter(is_published=True)

    if base_queryset is None:
        base_queryset = Course.objects.filter(is_published=True)

    # Перебираем только объекты из базового QuerySet
    result = [
        course for course in base_queryset if name.lower(
        ) in course.name.lower()
    ]

    # Создаём новый QuerySet с результатом, сохраняя тип
    queryset = base_queryset.none()  # пустой QuerySet того же типа
    queryset |= base_queryset.filter(
        id__in=[c.id for c in result]
    )  # добавляем найденные
    return queryset


def index(request):
    """
    Отображение главной страницы
    """
    return render(request, 'lesson/index.html')


def category_detail(request, slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=slug)
    courses = Course.objects.filter(category=category)
    return render(
        request,
        "lesson/courses_list.html",
        {"courses": courses, "categories": categories, "category": category}
    )


def courses_list(request, queryset=None):
    """
    Получение списка всех курсов или курсов по категориям
    """
    query_params = request.GET.urlencode()
    query_params_dict = query_params_in_dict(query_params)
    categories = Category.objects.all()
    if request.method == "POST":
        params = {}
        category = request.POST.getlist("category")

        if category:
            if len(category) > 1:
                params["category"] = ",".join(category)
                print(2, params)
            else:
                params["category"] = "".join(category)
        q = request.POST.get("q")
        if q:
            params["q"] = q
        url = f"{reverse('lesson:courses')}?{urlencode(params)}"
        return HttpResponseRedirect(url)

    selected_category_slugs = []
    if not query_params_dict:
        courses = Course.objects.prefetch_related().filter(is_published=True)
    else:
        courses = Course.objects.prefetch_related().filter(is_published=True)
        q = query_params_dict.get("q")
        category_param = query_params_dict.get("category")
        if q:
            courses = search_course_with_name(q, courses)
        if category_param:
            slugs = unquote(category_param).split(",")
            selected_category_slugs = slugs
            category_qs = Category.objects.filter(slug__in=slugs)

            courses = courses.filter(category__in=category_qs)

    context = {
        'courses': paginator(request, courses),
        "categories": categories,
        "selected_category_slugs": selected_category_slugs
    }

    return render(
        request,
        template_name='lesson/courses_list.html',
        context=context
    )


@login_required
def course_detail(request, course_name):
    """
    Получение модулей в курсе и прогресса прохождения курса
    """
    course = Course.objects.get(name=course_name)
    modules_user = Module.objects.filter(course=course)
    user_modules = []

    # Если в курсе не открыт первый урок, то открываем
    course_modules = list(course.modules.all())
    if course_modules:
        first_module = course_modules[0]
        first_module_lessons = list(first_module.lessons.all())
        if first_module_lessons:
            first_lesson = first_module_lessons[0]
            # Проверяем, есть ли уже прогресс по первому уроку
            first_lesson_exists = UserLessonProgress.objects.filter(
                user=request.user,
                course=course,
                module=first_module,
                lesson=first_lesson
            ).exists()
            
            if not first_lesson_exists:
                # Убираем флаг current у всех уроков этого курса
                UserLessonProgress.objects.filter(
                    user=request.user,
                    course=course
                ).update(current=False)
                
                # Создаем первый урок как текущий
                UserLessonProgress.objects.create(
                    user=request.user,
                    course=course,
                    module=first_module,
                    lesson=first_lesson,
                    current=True
                )

    total_lessons_count = 0
    total_completed_count = 0
    course_modules_list = list(course.modules.all())
    
    # Используем course_modules_list для правильного порядка модулей
    for module_index, module in enumerate(course_modules_list):
        lessons = module.lessons.all()
        total_lessons = lessons.count()
        total_lessons_count += total_lessons

        # Фильтруем прогресс по пользователю, курсу, модулю и уроку
        completed_lessons = UserLessonProgress.objects.filter(
            user=request.user,
            course=course,
            module=module,
            lesson__in=lessons,
            completed=True
        ).count()
        total_completed_count += completed_lessons

        # Рассчёт прогресса модуля
        progress = int(
            (completed_lessons / total_lessons) * 100
        ) if total_lessons > 0 else 0

        # Проверка доступности модуля
        is_available = False
        
        # Первый модуль всегда доступен
        if module_index == 0:
            is_available = True
        else:
            # Проверяем, пройден ли предыдущий модуль полностью
            try:
                prev_module = course_modules_list[module_index - 1]
                prev_module_lessons = prev_module.lessons.all()
                prev_completed_lessons = UserLessonProgress.objects.filter(
                    user=request.user,
                    course=course,
                    module=prev_module,
                    lesson__in=prev_module_lessons,
                    completed=True
                ).count()
                prev_total_lessons = prev_module_lessons.count()
                
                # Модуль доступен, если предыдущий модуль полностью пройден
                if prev_total_lessons > 0 and prev_completed_lessons == prev_total_lessons:
                    is_available = True
            except (IndexError, AttributeError):
                pass
        
        # Также модуль доступен, если в нем есть текущий урок
        if not is_available:
            has_current_lesson = UserLessonProgress.objects.filter(
                user=request.user,
                course=course,
                module=module,
                current=True
            ).exists()
            if has_current_lesson:
                is_available = True

        user_modules.append({
            'module': module,
            'progress': progress,
            'completed': progress == 100,
            'completed_lessons': completed_lessons,
            'total_lessons': total_lessons,
            'is_available': is_available,
        })
    
    # Общий прогресс курса - считаем только уроки этого курса у этого пользователя
    total_progress = int(
        (total_completed_count / total_lessons_count) * 100
    ) if total_lessons_count > 0 else 0
    # form = RegisterCourseForm(request.POST or None)
    # if request.method == 'POST':
    #     form_data = {
    #         'user': request.user,
    #         'course': course
    #     }
    #     RegisterCourse.objects.create(**form_data)
    #     return redirect('lesson:profile')
    # Расчет для SVG кругового прогресса (длина окружности = 2 * π * 15 ≈ 94.25)
    circle_circumference = 94.25
    circle_dasharray = (circle_circumference * total_progress / 100) if total_progress > 0 else 0
    
    context = {
        'course': course,
        'modules': user_modules,
        # 'form': form,
        "total_progress": total_progress,
        "total_lessons_count": total_lessons_count,
        "total_completed_count": total_completed_count,
        "circle_dasharray": circle_dasharray,
        "circle_circumference": circle_circumference,
    }
    return render(request, 'lesson/course_detail.html', context)


# @course_required
@login_required
def lesson_detail(request, course_name, module_name, lesson_name):
    """
    Просмотр материалов урока
    """
    course = Course.objects.get(name=course_name)
    module = Module.objects.get(title=module_name)
    lesson = Lesson.objects.get(title=lesson_name)
    try:
        les = UserLessonProgress.objects.get(
            user=request.user,
            course=course,
            module=module,
            lesson=lesson
        )
        if not (les.completed or les.current):
            return redirect(
                "lesson:module_detail",
                course_name, module_name
            )
    except Exception:
        return redirect(
            "lesson:module_detail",
            course_name, module_name
        )
    is_completed = UserLessonProgress.objects.get_or_create(
        user=request.user,
        course=course,
        module=module,
        lesson=lesson
    )[0].completed
    context = {
        'course_name': course_name,
        'module_name': module_name,
        'lesson_title': lesson_name,
        'lesson': lesson,
        "is_completed": is_completed,
    }
    return render(
        request,
        'lesson/lesson_detail.html',
        context=context
    )


@login_required
def module_detail(request, course_name, module_name):
    """
    Получение уроков в модуле. Открытие первого урока если модуль новый
    """
    course = Course.objects.get(name=course_name)
    module = Module.objects.get(title=module_name)
    
    # Проверка доступности модуля
    course_modules_list = list(course.modules.all())
    try:
        module_index = course_modules_list.index(module)
    except ValueError:
        # Модуль не найден в курсе - редирект на курс
        return redirect('lesson:course_detail', course_name=course_name)
    
    # Первый модуль всегда доступен
    if module_index > 0:
        # Проверяем, пройден ли предыдущий модуль полностью
        prev_module = course_modules_list[module_index - 1]
        prev_module_lessons = prev_module.lessons.all()
        prev_completed_lessons = UserLessonProgress.objects.filter(
            user=request.user,
            course=course,
            module=prev_module,
            lesson__in=prev_module_lessons,
            completed=True
        ).count()
        prev_total_lessons = prev_module_lessons.count()
        
        # Если предыдущий модуль не пройден полностью и в текущем модуле нет текущего урока
        if prev_total_lessons > 0 and prev_completed_lessons != prev_total_lessons:
            has_current_lesson = UserLessonProgress.objects.filter(
                user=request.user,
                course=course,
                module=module,
                current=True
            ).exists()
            
            if not has_current_lesson:
                # Модуль заблокирован - редирект на курс
                return redirect('lesson:course_detail', course_name=course_name)
    
    lessons_module = module.lessons.all()

    # Если в модуле не открыт первый урок, назначаем его текущим
    # if module.lessons.all()[0].id not in UserLessonProgress.objects.filter(
    #         user=request.user
    # ).values_list("lesson_id", flat=True):
    #     print(request.user, module.lessons.all()[0])
    #     UserLessonProgress.objects.create(
    #         user=request.user,
    #         course=course,
    #         module=module,
    #         lesson=module.lessons.all()[0],
    #         current=True
    #     )

    # Получаем список уроков в модуле + пройден,
    # текущий или закрыт (Закрыт если записи нет)
    lessons = []
    for lesson in lessons_module:
        try:
            current_lesson = UserLessonProgress.objects.get(
                user=request.user,
                course=course,
                module=module,
                lesson=lesson
            )
            is_completed = current_lesson.completed
            is_current = current_lesson.current
        except Exception:
            is_completed = False
            is_current = False

        lessons.append({
            'lesson': lesson,
            'is_completed': is_completed,
            'is_current': is_current,
        })

    context = {
        'lessons': lessons,
        'course_name': course_name,
        'module_name': module_name
    }
    return render(request, 'lesson/module_detail.html', context)


@login_required
def complete_lesson(request, course_name, module_name, lesson_name):
    """
    Отметка урока как пройденного и открытие следующего урока.
    Логика:
    1. Отмечаем текущий урок как завершенный
    2. Убираем флаг current у всех уроков этого пользователя в этом курсе
    3. Открываем следующий урок:
       - Если есть следующий урок в модуле - открываем его
       - Если это последний урок в модуле - открываем первый урок следующего модуля
       - Если это последний урок в последнем модуле - курс завершен
    """
    course = Course.objects.get(name=course_name)
    module = Module.objects.get(title=module_name)
    lesson = Lesson.objects.get(title=lesson_name)
    
    # 1. Отметить текущий урок как завершённый
    progress, created = UserLessonProgress.objects.get_or_create(
        user=request.user,
        course=course,
        module=module,
        lesson=lesson,
    )
    progress.completed = True
    progress.current = False
    progress.save()
    
    # 2. Убрать флаг current у всех уроков этого пользователя в этом курсе
    UserLessonProgress.objects.filter(
        user=request.user,
        course=course
    ).update(current=False)
    
    # 3. Найти следующий урок
    module_lessons = list(module.lessons.all())
    course_modules = list(course.modules.all())
    
    # Получаем индекс текущего урока в модуле
    try:
        current_lesson_index = module_lessons.index(lesson)
    except ValueError:
        # Если урока нет в списке, редиректим на модуль
        return redirect(
            'lesson:module_detail',
            course_name=course_name,
            module_name=module_name
        )
    
    next_module = None
    next_lesson = None
    
    # Проверяем, есть ли следующий урок в текущем модуле
    if current_lesson_index + 1 < len(module_lessons):
        # Есть следующий урок в том же модуле
        next_lesson = module_lessons[current_lesson_index + 1]
        next_module = module
    else:
        # Это последний урок в модуле - ищем следующий модуль
        try:
            current_module_index = course_modules.index(module)
            if current_module_index + 1 < len(course_modules):
                # Есть следующий модуль
                next_module = course_modules[current_module_index + 1]
                next_module_lessons = list(next_module.lessons.all())
                if next_module_lessons:
                    next_lesson = next_module_lessons[0]
        except ValueError:
            pass
    
    # 4. Открыть следующий урок, если он найден
    if next_lesson and next_module:
        next_progress, created = UserLessonProgress.objects.get_or_create(
            user=request.user,
            course=course,
            module=next_module,
            lesson=next_lesson,
        )
        next_progress.current = True
        next_progress.save()
        
        # Редирект на модуль следующего урока
        return redirect(
            'lesson:module_detail',
            course_name=course_name,
            module_name=next_module.title
        )
    
    # Курс завершен или следующий урок не найден - остаемся в текущем модуле
    return redirect(
        'lesson:module_detail',
        course_name=course_name,
        module_name=module_name
    )


@login_required
def profile(request):
    """
    Профиль пользователя. Отображение роли, проходимый и преподаваемых курсов
    """
    # queryset = RegisterCourse.objects.filter(user=request.user)
    user = request.user
    result = ''
    if user.is_superuser:
        result += 'Модератор '
    if user.is_teacher:
        result += 'Преподаватель '
    if user.is_student:
        result += 'Студент '
    is_teacher = user.is_teacher
    is_student = user.is_student
    result = result.strip()
    result = result.replace(' ', ' & ')
    # learn_courses = user.courses_learn.all()
    # teach_courses = user.courses_teach.all()
    cancelled_lesson = CancelledLesson.objects.filter(student=request.user)
    cancelled = [elem.date_cancelled.day for elem in cancelled_lesson]

    lessons_time = Schedule.objects.filter(student=request.user)
    weekdays = [elem.weekday for elem in lessons_time]

    current_year = datetime.today().year
    current_month = datetime.today().month

    month_matrix = calendar.monthcalendar(current_year, current_month)

    context = {
        # 'learn_courses': learn_courses,
        # 'teach_courses': teach_courses,
        'result': result,
        'user': user,
        'is_teacher': is_teacher,
        'is_student': is_student,
        'is_tutor_student': user.is_tutor_student,
        # 'queryset': queryset,
        'month_matrix': month_matrix,
        'current_day': datetime.today().day,
        'weekdays': weekdays,
        'cancelled': cancelled,
    }

    return render(request, 'lesson/profile.html', context)


# @login_required
# @require_http_methods(["GET", "POST"])
# def upload_image(request):
#     """
#     Endpoint для загрузки изображений в Editor.js
#     """
#     if request.method == 'POST':
#         if 'image' not in request.FILES:
#             return JsonResponse({'success': 0, 'error': 'Файл не найден'}, status=400)
#
#         image_file = request.FILES['image']
#
#         # Проверка типа файла
#         allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
#         if image_file.content_type not in allowed_types:
#             return JsonResponse({
#                 'success': 0,
#                 'error': 'Неподдерживаемый формат изображения. Разрешены: JPG, PNG, GIF, WebP'
#             }, status=400)
#
#         # Проверка размера файла (максимум 10 МБ)
#         max_size = 10 * 1024 * 1024  # 10 МБ
#         if image_file.size > max_size:
#             return JsonResponse({
#                 'success': 0,
#                 'error': f'Файл слишком большой. Максимальный размер: 10 МБ'
#             }, status=400)
#
#         # Сохранение файла
#         try:
#             # Генерируем уникальное имя файла
#             file_extension = image_file.name.split('.')[-1] if '.' in image_file.name else 'jpg'
#             unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
#
#             # Создаем путь с датой для организации файлов
#             date_path = datetime.now().strftime('%Y/%m/%d')
#             file_path = default_storage.save(
#                 f'editorjs/{date_path}/{unique_filename}',
#                 ContentFile(image_file.read())
#             )
#
#             # Получаем URL файла
#             file_url = default_storage.url(file_path)
#
#             # Убеждаемся, что URL начинается с правильного пути
#             if not file_url.startswith('http') and not file_url.startswith('/'):
#                 file_url = '/' + file_url.lstrip('/')
#
#             return JsonResponse({
#                 'success': 1,
#                 'url': file_url
#             })
#         except Exception as e:
#             import traceback
#             print(f"Ошибка загрузки изображения: {e}")
#             print(traceback.format_exc())
#             return JsonResponse({
#                 'success': 0,
#                 'error': f'Ошибка при сохранении файла: {str(e)}'
#             }, status=500)
#
#     return JsonResponse({'success': 0, 'error': 'Метод не разрешен'}, status=405)
#
#
# @login_required
# def lesson_create(request):
#     """
#     Создание нового урока с блочным редактором
#     """
#     if request.method == 'POST':
#         form = CreateLessonForm(request.POST)
#         if form.is_valid():
#             lesson = form.save()
#             return redirect('lesson:lesson_edit', lesson_id=lesson.id)
#     else:
#         form = CreateLessonForm()
#
#     context = {
#         'form': form,
#         'lesson': None,
#     }
#     return render(request, 'lesson/lesson_edit.html', context)
#
#
# @login_required
# def lesson_edit(request, lesson_id):
#     """
#     Редактирование урока с блочным редактором
#     """
#     try:
#         lesson = Lesson.objects.get(id=lesson_id)
#     except Lesson.DoesNotExist:
#         return redirect('lesson:courses')
#
#     if request.method == 'POST':
#         form = CreateLessonForm(request.POST, instance=lesson)
#         if form.is_valid():
#             form.save()
#             return redirect('lesson:courses')
#     else:
#         form = CreateLessonForm(instance=lesson)
#
#     context = {
#         'form': form,
#         'lesson': lesson,
#     }
#     return render(request, 'lesson/lesson_edit.html', context)


@login_required
def profile_edit(request):
    """
    Редактирование профайла
    """
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if request.FILES.get('image'):
                user.image = request.FILES['image']
            user.save()
            return redirect('lesson:profile')
    else:
        form = EditProfile(instance=request.user)
    return render(request, 'lesson/profile_edit.html', {'form': form})


def course_editor(request):
    pass
