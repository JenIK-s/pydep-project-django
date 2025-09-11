from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

from .models import FilesProject, Lesson
from .forms import LessonForm, PaymentUpdateForm


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


def schedule(request):
    lessons = Lesson.objects.select_related('teacher', 'student').all()
    teacher_lessons = lessons  # пока без ограничений, как просили
    student_lessons = lessons
    context = {
        'teacher_lessons': teacher_lessons,
        'student_lessons': student_lessons,
    }
    return render(request, 'tutor/schedule.html', context)


def lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            # Повтор по неделям до конечной даты, зависящей от периода
            repeat = form.cleaned_data.get('repeat_period')
            if repeat:
                months = {"1m": 1, "6m": 6, "12m": 12}.get(repeat, 0)
                if months:
                    end_date = lesson.date + relativedelta(months=+months)
                    current_date = lesson.date + timedelta(weeks=1)
                    while current_date <= end_date:
                        Lesson.objects.create(
                            teacher=lesson.teacher,
                            student=lesson.student,
                            subject=lesson.subject,
                            date=current_date,
                            start_time=lesson.start_time,
                            end_time=lesson.end_time,
                            lesson_format=lesson.lesson_format,
                            comment=lesson.comment,
                            status=lesson.status,
                            is_paid=False,
                        )
                        current_date += timedelta(weeks=1)
            return redirect(reverse('tutor:schedule'))
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['teacher'] = request.user
        form = LessonForm(initial=initial)
    return render(request, 'tutor/lesson_form.html', {'form': form, 'title': 'Новое занятие'})


def lesson_update(request, pk: int):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect(reverse('tutor:schedule'))
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'tutor/lesson_form.html', {'form': form, 'title': 'Редактировать занятие'})


def lesson_payment_toggle(request, pk: int):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = PaymentUpdateForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect(reverse('tutor:schedule'))
    else:
        form = PaymentUpdateForm(instance=lesson)
    return render(request, 'tutor/lesson_payment.html', {'form': form, 'lesson': lesson})
