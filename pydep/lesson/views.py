from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Course, ModulesInCourse, Module, Lesson


def index(request):
    return render(request, 'lesson/index.html')


@login_required
def courses_list(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'lesson/courses_list.html', context)


@login_required
def course_detail(request, course_name):
    course = Course.objects.get(name=course_name)
    modules = ModulesInCourse.objects.filter(course=course)
    context = {
        'course': course,
        'modules': modules,
    }
    return render(request, 'lesson/course_detail.html', context)


@login_required
def lesson_detail(request, course_name, lesson_title):
    return render(request, 'lesson/lesson_detail.html')


@login_required
def module_detail(request, module_name):
    lessons_list = Module.objects.filter(title=module_name)
    lessons_values = None
    for les in lessons_list:
        lessons_values = les.lessons.values_list('title', flat=True)
    lessons = []
    for lesson in lessons_values:
        lessons.append(Lesson.objects.filter(title=lesson))
    for l in lessons:
        print(l.values('title'))

    context = {
        'lessons': lessons
    }
    return render(request, 'lesson/module_detail.html', context)



@login_required
def profile(request):
    return render(request, 'lesson/profile.html')
