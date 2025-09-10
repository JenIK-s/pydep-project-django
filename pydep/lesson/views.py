import calendar
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

from .context_processors.bot import send_message
from .context_processors.decorators import search_request
from .forms import RegisterCourseForm
from .forms import EditProfile
from .forms import CreateLessonForm
from .models import Course
from .models import ModulesInCourse
from .models import Module
from .models import Lesson
from .models import Category
from users.models import CancelledLesson
from users.models import RegisterCourse
from users.models import Schedule



def get_weekday(day):
    year = datetime.today().year
    month = datetime.today().month
    date_string = f"{year}-{month:02d}-{day:02d}"
    date = datetime.strptime(date_string, "%Y-%m-%d")
    weekday_name = date.strftime("%A")

    return weekday_name


def index(request):
    """
    Отображение главной страницы
    """
    return render(request, 'lesson/index.html')


def category_detail(request, slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=slug)
    courses = Course.objects.filter(category=category)
    return render(request, "lesson/courses_list.html", {"courses": courses, "categories": categories, "category": category})


@search_request
def courses_list(request, queryset=None):
    """
    Получение списка всех курсов или курсов по категориям
    """
    categories = Category.objects.all()
    if queryset is None:
        context = {'courses': Course.objects.all(), "categories": categories}
    else:
        context = {'courses': queryset, "categories": categories}
    return render(request, template_name='lesson/courses_list.html',
                  context=context)


@search_request
@login_required
def courses_list_about_languages(request, prog_lang, queryset=None):
    if queryset is None:
        context = {
            'courses': Course.objects.filter(programming_language=prog_lang)
        }
    else:
        context = {'courses': queryset}
    return render(
        request, template_name='lesson/courses_list_about_languages.html',
        context=context
    )


@login_required
def course_detail(request, course_name):
    """
    Получение модулей в курсе и прогресса прохождения курса
    """
    course = Course.objects.get(name=course_name)
    modules = ModulesInCourse.objects.filter(course=course)
    modules_user = Module.objects.filter(course=course)
    user_modules = []
    total_lessons_count = 0
    total_completed_count = 0
    for module in modules_user:
        lessons = module.lessons.all()
        total_lessons = lessons.count()
        total_lessons_count += total_lessons

        completed_lessons = UserLessonProgress.objects.filter(
            user=request.user,
            lesson__in=lessons,
            completed=True
        ).count()
        total_completed_count += completed_lessons

        # Рассчёт прогресса
        progress = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0

        user_modules.append({
            'module': module,
            'progress': progress,
            'completed': progress == 100,
        })
    total_progress = int((total_completed_count / total_lessons_count) * 100) if total_lessons_count > 0 else 0
    form = RegisterCourseForm(request.POST or None)
    if request.method == 'POST':
        form_data = {
            'user': request.user,
            'course': course
        }
        RegisterCourse.objects.create(**form_data)
        send_message('861963780', f'Вы отправили заявку на курс {course.name}.')
        return redirect('lesson:profile')
    context = {
        'course': course,
        'modules': user_modules,
        'form': form,
        "total_progress": total_progress,
        "circle_clip": 100 - total_progress,
    }
    return render(request, 'lesson/course_detail.html', context)


# @course_required
@login_required
def lesson_detail(request, course_name, module_name, lesson_name):
    """
    Просмотр материалов урока
    """

    lesson = Lesson.objects.get(title=lesson_name)
    try:
        les = UserLessonProgress.objects.get(user=request.user, lesson=lesson)
        print("TRY")
        if not (les.completed or les.current):
            print("IF")
            return redirect("lesson:module_detail", course_name, module_name)
    except:
        print("EXCEPT")
        return redirect("lesson:module_detail", course_name, module_name)
    is_completed = UserLessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )[0].completed
    context = {
        'course_name': course_name,
        'module_name': module_name,
        'lesson_title': lesson_name,
        'lesson': lesson,
        "is_completed": is_completed,
    }
    return render(request, 'lesson/lesson_detail.html', context=context)


@login_required
def module_detail(request, course_name, module_name):
    """
    Получение уроков в модуле. Открытие первого урока если модуль новый
    """
    course = Course.objects.get(name=course_name)
    module = Module.objects.get(title=module_name)
    lessons_module = module.lessons.all()

    # Если в модуле не открыт первый урок, назначаем его текущим
    if module.lessons.all()[0].id not in UserLessonProgress.objects.filter(user=request.user).values_list("lesson_id", flat=True):
        UserLessonProgress.objects.create(
            user=request.user,
            lesson=module.lessons.all()[0],
            current=True
        )

    # Получаем список уроков в модуле + пройден, текущий или закрыт (Закрыт если записи нет)
    lessons = []
    for lesson in lessons_module:
        try:
            print(1)
            current_lesson = UserLessonProgress.objects.get(course=course, module=module, lesson=lesson)
            is_completed = current_lesson.completed
            is_current = current_lesson.current
            print(current_lesson, is_completed, is_current)
        except:
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
    Отметка урока как пройденного и открытие следующего не пройденного урока
    """
    course = Course.objects.get(name=course_name)
    module = Module.objects.get(title=module_name)
    lesson = Lesson.objects.get(title=lesson_name)

    # Отметить текущий как завершённый
    progress, created = UserLessonProgress.objects.get_or_create(
        user=request.user,
        course=course,
        module=module,
        lesson=lesson,

    )
    progress.completed = True
    progress.current = False
    progress.save()

    # Найти следующий урок
    next_lesson = None
    module = Module.objects.get(title=module_name)
    module_lessons = module.lessons.all()
    for i in range(len(module_lessons) - 1):
        # Если текущий урок пройден, а следующего нет в таблице прогресса, то открываем следующий
        if UserLessonProgress.objects.get(course=course, module=module, lesson=lesson).completed and UserLessonProgress.objects.filter(course=course, module=module, lesson=module_lessons[i + 1]).first() is None:

            next_progress, created = UserLessonProgress.objects.get_or_create(
                user=request.user,
                course=course,
                module=module,
                lesson=module_lessons[i + 1]
            )
            next_progress.current = True
            next_progress.save()
            break

    return redirect('lesson:module_detail', course_name=course_name, module_name=module_name)


@login_required
def profile(request):
    """
    Профиль пользователя. Отображение роли, проходимый и преподаваемых курсов
    """
    queryset = RegisterCourse.objects.filter(user=request.user)
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
    learn_courses = user.courses_learn.all()
    teach_courses = user.courses_teach.all()
    cancelled_lesson = CancelledLesson.objects.filter(student=request.user)
    cancelled = [elem.date_cancelled.day for elem in cancelled_lesson]

    lessons_time = Schedule.objects.filter(student=request.user)
    weekdays = [elem.weekday for elem in lessons_time]

    current_year = datetime.today().year
    current_month = datetime.today().month

    month_matrix = calendar.monthcalendar(current_year, current_month)

    context = {
        'learn_courses': learn_courses,
        'teach_courses': teach_courses,
        'result': result,
        'user': user,
        'is_teacher': is_teacher,
        'is_student': is_student,
        'is_tutor_student': user.is_tutor_student,
        'queryset': queryset,
        'month_matrix': month_matrix,
        'current_day': datetime.today().day,
        'weekdays': weekdays,
        'cancelled': cancelled,
    }

    return render(request, 'lesson/profile.html', context)


def schedule_today(request, day):
    weekday = get_weekday(int(day))
    print(weekday)
    lesson = Schedule.objects.get(student=request.user, weekday=weekday)
    context = {
        'data': f'{day}.{datetime.today().month}.{datetime.today().year}',
        'time': lesson.time_start,
        'hour_amount': lesson.hour_amount
    }

    return render(request, 'lesson/profile_tutor_student.html', context)

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


def register_course_admin(request):
    """
    Обработка заявок на курсы
    """
    queryset = RegisterCourse.objects.all()
    if request.method == 'POST':
        result = request.POST.get('action').split('_')
        operation, register_id = result
        course = RegisterCourse.objects.filter(pk=register_id)
        match operation:
            case 'ap':
                try:
                    course_object = course.first().course
                    course.first().user.courses_learn.add(course_object)
                    course.update(status="approved")
                    send_message('861963780', 'Ваша заявка ОДОБРЕНА')
                except:
                    return HttpResponse(404)
            case 'rj':
                course.update(status="rejected")
                send_message('861963780', 'Ваша заявка ОТКОЛНЕНА')
            case 'dl':
                course.delete()
        return redirect('lesson:register_course_admin')
    return render(request, 'lesson/register_course_admin.html', {'queryset': queryset})


def register_course(request):
    queryset = RegisterCourse.objects.filter(user=request.user)
    return render(request, 'lesson/register_course.html', {'queryset': queryset})


def tutor_students(request):
    queryset = RegisterCourse.objects.filter(user=request.user)
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
    learn_courses = user.courses_learn.all()
    teach_courses = user.courses_teach.all()
    cancelled_lesson = CancelledLesson.objects.filter(student=request.user)
    cancelled = [elem.date_cancelled.day for elem in cancelled_lesson]

    lessons_time = Schedule.objects.filter(student=request.user)
    weekdays = [elem.weekday for elem in lessons_time]

    current_year = datetime.today().year
    current_month = datetime.today().month

    month_matrix = calendar.monthcalendar(current_year, current_month)

    context = {
        'learn_courses': learn_courses,
        'teach_courses': teach_courses,
        'result': result,
        'user': user,
        'is_teacher': is_teacher,
        'is_student': is_student,
        'is_tutor_student': user.is_tutor_student,
        'queryset': queryset,
        'month_matrix': month_matrix,
        'current_day': datetime.today().day,
        'weekdays': weekdays,
        'cancelled': cancelled,
    }
    return render(request, "lesson/tutor_students.html", context)


def create_lesson(request):
    if request.method == "POST":
        print(123)
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateLessonForm()
    return render(request, "lesson/create_lesson.html", {"form": form})


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import ProjectDocument

def projects(request):
    projects = ProjectDocument.objects.all()
    return render(request, "lesson/projects.html", {"projects": projects})

def projects_detail(request, name):
    project = get_object_or_404(ProjectDocument, name=name)
    with project.file.open('r') as f:
        html_content = f.read()
    return HttpResponse(html_content)
