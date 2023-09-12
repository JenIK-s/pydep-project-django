from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Course, ModulesInCourse, Module, Lesson

from .context_processors.decorators import course_required


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
def courses_list_about_languages(request, prog_lang):
    courses = Course.objects.filter(programming_language=prog_lang)
    context = {
        'courses': courses,
    }
    return render(
        request,
        template_name='lesson/courses_list_about_languages.html',
        context=context
    )


@course_required
@login_required
def course_detail(request, course_name):
    course = Course.objects.get(name=course_name)
    modules = ModulesInCourse.objects.filter(course=course)
    context = {
        'course': course,
        'modules': modules,
    }
    return render(request, 'lesson/course_detail.html', context)


@course_required
@login_required
def lesson_detail(request, course_name, module_name, lesson_name):
    lesson = Lesson.objects.get(title=lesson_name)
    context = {
        'course_name': course_name,
        'module_name': module_name,
        'lesson_title': lesson_name,
        'lesson': lesson,
    }
    return render(request, 'lesson/lesson_detail.html', context=context)


@course_required
@login_required
def module_detail(request, course_name, module_name):
    module = Module.objects.get(title=module_name)
    lessons = module.lessons.all()

    context = {
        'lessons': lessons,
        'course_name': course_name,
        'module_name': module.title
    }
    return render(request, 'lesson/module_detail.html', context)


@login_required
def profile(request):
    user = request.user
    is_teacher = user.is_teacher
    is_student = user.is_student
    learn_courses = user.courses_learn.all()
    teach_courses = user.courses_teach.all()
    print(learn_courses)
    context = {
        'learn_courses': learn_courses,
        'teach_courses': teach_courses,
        'is_teacher': is_teacher,
        'is_student': is_student,
    }
    return render(request, 'lesson/profile.html', context)
