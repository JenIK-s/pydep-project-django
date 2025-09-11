from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import FilesProject


def my_tutor(request):
    return render(request, "tutor/my_tutor.html")


def projectbox(request):
    files = FilesProject.objects.all()
    return render(request, "tutor/projectbox.html", {"files": files})


@login_required
def profile(request):
    """
    Профиль пользователя. Отображение роли, проходимый и преподаваемых курсов
    """
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


    context = {
        'result': result,
        'user': user,
        'is_teacher': is_teacher,
        'is_student': is_student,
        'is_tutor_student': user.is_tutor_student,
    }

    return render(request, 'tutor/profile.html', context)
