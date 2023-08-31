from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Course, ModulesInCourse


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
def profile(request):
    return render(request, 'lesson/profile.html')
