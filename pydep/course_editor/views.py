import uuid
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import  JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .forms import CreateLessonForm
from lesson.models import Lesson


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
            lesson = form.save()
            return redirect('course_editor:lesson_edit', lesson_id=lesson.id)
    else:
        form = CreateLessonForm()

    context = {
        'form': form,
        'lesson': None,
    }
    return render(request, 'course_editor/lesson_edit.html', context)


@login_required
def lesson_edit(request, lesson_id):
    """
    Редактирование урока с блочным редактором
    """
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return redirect('course_editor:courses')

    if request.method == 'POST':
        form = CreateLessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('course_editor:courses')
    else:
        form = CreateLessonForm(instance=lesson)

    context = {
        'form': form,
        'lesson': lesson,
    }
    return render(request, 'course_editor/lesson_edit.html', context)


def course_editor_main(request):
    return render(request, "course_editor/course_editor_main.html")
