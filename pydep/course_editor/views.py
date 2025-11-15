import uuid
import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .forms import CreateLessonForm, CourseForm, ModuleForm
from lesson.models import (
    Lesson,
    Module,
    Course,
    ModulesInCourse,
    LessonsInModule,
)


@login_required
@require_http_methods(["GET", "POST"])
def upload_image(request):
    """
    Endpoint для загрузки изображений в Editor.js
    """
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({'success': 0, 'error': 'Файл не найден'}, status=400)

        image_file = request.FILES['image']

        # Проверка типа файла
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if image_file.content_type not in allowed_types:
            return JsonResponse({
                'success': 0,
                'error': 'Неподдерживаемый формат изображения. Разрешены: JPG, PNG, GIF, WebP'
            }, status=400)

        # Проверка размера файла (максимум 10 МБ)
        max_size = 10 * 1024 * 1024  # 10 МБ
        if image_file.size > max_size:
            return JsonResponse({
                'success': 0,
                'error': f'Файл слишком большой. Максимальный размер: 10 МБ'
            }, status=400)

        # Сохранение файла
        try:
            # Генерируем уникальное имя файла
            file_extension = image_file.name.split('.')[-1] if '.' in image_file.name else 'jpg'
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

            # Создаем путь с датой для организации файлов
            date_path = datetime.now().strftime('%Y/%m/%d')
            file_path = default_storage.save(
                f'editorjs/{date_path}/{unique_filename}',
                ContentFile(image_file.read())
            )

            # Получаем URL файла
            file_url = default_storage.url(file_path)

            # Убеждаемся, что URL начинается с правильного пути
            if not file_url.startswith('http') and not file_url.startswith('/'):
                file_url = '/' + file_url.lstrip('/')

            return JsonResponse({
                'success': 1,
                'url': file_url
            })
        except Exception as e:
            import traceback
            print(f"Ошибка загрузки изображения: {e}")
            print(traceback.format_exc())
            return JsonResponse({
                'success': 0,
                'error': f'Ошибка при сохранении файла: {str(e)}'
            }, status=500)

    return JsonResponse({'success': 0, 'error': 'Метод не разрешен'}, status=405)


@login_required
def lesson_create(request):
    """
    Создание нового урока с блочным редактором
    """
    if request.method == 'POST':
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.save()
            lesson.authors.add(request.user)
            # Проверяем, откуда пришли (из модуля или нет)
            return_to_module = request.session.get('return_to_module_after_lesson')
            if return_to_module:
                del request.session['return_to_module_after_lesson']
                messages.success(request, f'Урок «{lesson.title}» создан. Теперь добавьте его в модуль.')
                return redirect(f"{reverse('studio:module_create')}?lesson_id={lesson.id}")
            messages.success(request, f'Урок «{lesson.title}» успешно создан.')
            return redirect('studio:main')
    else:
        form = CreateLessonForm()
        # Сохраняем в session, что нужно вернуться к модулю
        if request.GET.get('module_id'):
            request.session['return_to_module_after_lesson'] = True

    context = {
        'form': form,
        'lesson': None,
    }
    return render(request, 'course_editor/lesson_edit.html', context)


@login_required
def lesson_edit(request, course_id, module_id, lesson_id):
    """
    Редактирование урока с блочным редактором
    """
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return redirect('studio:main')

    if request.method == 'POST':
        form = CreateLessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('studio:main')
    else:
        form = CreateLessonForm(instance=lesson)

    context = {
        'form': form,
        'lesson': lesson,
    }
    return render(request, 'course_editor/lesson_edit.html', context)


@login_required
def course_create(request):
    """
    Создание нового курса - только основная информация
    """
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            course.authors.add(request.user)
            messages.success(request, f'Курс «{course.name}» успешно создан.')
            return redirect('lesson:course_detail', course_name=course.name)
    else:
        form = CourseForm()

    context = {
        'form': form,
    }
    return render(request, 'course_editor/course_create.html', context)


@login_required
def course_edit(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect('studio:course_create')

    if request.method == 'POST':
        # Публикация курса
        if 'toggle_publish' in request.POST:
            course.is_published = not course.is_published
            course.save()
            status_text = 'опубликован' if course.is_published else 'скрыт'
            if status_text == "опубликован":
                messages.success(request, f'Курс «{course.name}» успешно {status_text}.')
            elif status_text == "скрыт":
                messages.warning(request, f'Курс «{course.name}» успешно {status_text}.')

            return redirect('studio:course_edit', course_id=course.id)

        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save()
            
            # Обработка модулей: получаем порядок из скрытого поля
            modules_order = request.POST.get('modules_order', '')
            # Удаляем все существующие связи модулей с курсом
            ModulesInCourse.objects.filter(course=course).delete()
            
            if modules_order:
                # Парсим порядок модулей (список ID через запятую)
                module_ids = [int(id.strip()) for id in modules_order.split(',') if id.strip().isdigit()]
                
                # Создаем новые связи в правильном порядке
                for sequence_number, module_id in enumerate(module_ids, start=1):
                    try:
                        module = Module.objects.get(id=module_id)
                        # Проверяем, что модуль принадлежит текущему пользователю
                        if request.user in module.authors.all():
                            ModulesInCourse.objects.create(
                                course=course,
                                module=module,
                                sequence_number=sequence_number
                            )
                    except Module.DoesNotExist:
                        continue

            # Обработка переключения статуса публикации

            
            messages.success(request, f'Курс «{course.name}» успешно обновлен.')
            return redirect('studio:course_edit', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    # Получаем модули авторизованного пользователя
    modules = request.user.authored_modules.all()
    
    # Получаем модули, уже добавленные в курс, с их порядком
    existing_modules_in_course = ModulesInCourse.objects.filter(
        course=course
    ).select_related('module').order_by('sequence_number')
    existing_module_ids = [mic.module.id for mic in existing_modules_in_course]
    
    context = {
        'form': form,
        'course': course,
        'modules': modules,
        'existing_module_ids': existing_module_ids or [],
    }
    return render(request, 'course_editor/course_create.html', context)


@login_required
def module_create(request, course_id):
    """
    Создание нового модуля - информация о модуле и выбор уроков
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect('studio:main')
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            module = form.save(commit=False)
            module.save()
            module.authors.add(request.user)
            
            # Обработка уроков: получаем порядок из скрытого поля
            lessons_order = request.POST.get('lessons_order', '')
            if lessons_order:
                # Парсим порядок уроков (список ID через запятую)
                lesson_ids = [int(id.strip()) for id in lessons_order.split(',') if id.strip().isdigit()]
                
                # Создаем связи в правильном порядке
                for sequence_number, lesson_id in enumerate(lesson_ids, start=1):
                    try:
                        lesson = Lesson.objects.get(id=lesson_id)
                        # Проверяем, что урок принадлежит текущему пользователю
                        if request.user in lesson.authors.all():
                            LessonsInModule.objects.create(
                                module=module,
                                lesson=lesson,
                                sequence_number=sequence_number
                            )
                    except Lesson.DoesNotExist:
                        continue
            
            messages.success(request, f'Модуль «{module.title}» успешно создан.')
            return redirect('studio:course_edit', course_id=course.id)
    else:
        form = ModuleForm()
        # Сохраняем в session, что нужно вернуться к курсу
        if request.GET.get('course_id'):
            request.session['return_to_course_after_module'] = True
        # Если передан lesson_id, предварительно выбираем этот урок
        lesson_id = request.GET.get('lesson_id')
        if lesson_id:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                form.fields['lessons'].initial = [lesson.id]
            except Lesson.DoesNotExist:
                pass

    # Получаем уроки авторизованного пользователя
    lessons = request.user.authored_lessons.all()
    
    context = {
        'form': form,
        'course': course,
        'lessons': lessons,
        'existing_lesson_ids': [],
    }
    return render(request, 'course_editor/module_create.html', context)


@login_required
def module_edit(request, course_id, module_id):
    try:
        module = Module.objects.get(id=module_id)
        course = Course.objects.get(id=course_id)
    except (Module.DoesNotExist, Course.DoesNotExist):
        return redirect('studio:main')

    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES, instance=module)
        if form.is_valid():
            module = form.save()
            
            # Обработка уроков: получаем порядок из скрытого поля
            lessons_order = request.POST.get('lessons_order', '')
            # Удаляем все существующие связи уроков с модулем
            LessonsInModule.objects.filter(module=module).delete()
            
            if lessons_order:
                # Парсим порядок уроков (список ID через запятую)
                lesson_ids = [int(id.strip()) for id in lessons_order.split(',') if id.strip().isdigit()]
                
                # Создаем новые связи в правильном порядке
                for sequence_number, lesson_id in enumerate(lesson_ids, start=1):
                    try:
                        lesson = Lesson.objects.get(id=lesson_id)
                        # Проверяем, что урок принадлежит текущему пользователю
                        if request.user in lesson.authors.all():
                            LessonsInModule.objects.create(
                                module=module,
                                lesson=lesson,
                                sequence_number=sequence_number
                            )
                    except Lesson.DoesNotExist:
                        continue
            
            messages.success(request, f'Модуль «{module.title}» успешно обновлен.')
            return redirect('studio:course_edit', course_id=course.id)
    else:
        form = ModuleForm(instance=module)
    
    # Получаем уроки авторизованного пользователя
    lessons = request.user.authored_lessons.all()
    
    # Получаем уроки, уже добавленные в модуль, с их порядком
    existing_lessons_in_module = LessonsInModule.objects.filter(
        module=module
    ).select_related('lesson').order_by('sequence_number')
    existing_lesson_ids = [lim.lesson.id for lim in existing_lessons_in_module]
    
    context = {
        'form': form,
        'module': module,
        'course': course,
        'lessons': lessons,
        'existing_lesson_ids': existing_lesson_ids or [],
    }
    return render(request, 'course_editor/module_create.html', context)


@login_required
def course_editor_main(request):
    return render(request, "course_editor/course_editor_main.html")


def my_courses(request):
    courses = request.user.authored_courses.all()
    return render(request, "course_editor/my_courses.html", {"courses": courses})
