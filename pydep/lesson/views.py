from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Course, ModulesInCourse, Module, Lesson
from .forms import RegisterCourseForm, EditProfile
from .context_processors.bot import send_message
from .context_processors.decorators import course_required, search_request
from users.models import RegisterCourse
import os


def index(request):
    return render(request, 'lesson/index.html')


@search_request
def courses_list(request, queryset=None):
    if queryset is None:
        context = {'courses': Course.objects.all()}
    else:
        context = {'courses': queryset}

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
    course = Course.objects.get(name=course_name)
    modules = ModulesInCourse.objects.filter(course=course)
    form = RegisterCourseForm(request.POST or None)

    if form.is_valid():
        application = form.save(commit=False)
        form_data = {
            'user': request.user,
            'course': course,
            'start_date': application.start_date
        }
        print(form_data)
        RegisterCourse.objects.create(**form_data)
        send_message('861963780', f'Вы отправили заявку на курс {course.name}.')
        return redirect('lesson:profile')

    context = {
        'course': course,
        'modules': modules,
        'form': form,
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

    context = {
        'learn_courses': learn_courses,
        'teach_courses': teach_courses,
        'is_teacher': is_teacher,
        'is_student': is_student,
        'user': user,
    }
    return render(request, 'lesson/profile.html', context)


def profile_edit(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.FILES.get('image', None):
                request.user.image = request.FILES['image']
            if request.FILES.get('email', None):
                request.user.email = request.FILES['email']
            if request.FILES.get('background_image', None):
                request.user.background_image = request.FILES['background_image']
            if request.FILES.get('description', None):
                request.user.description = request.FILES['description']
            request.user.save()
            return redirect('lesson:profile')
    else:
        form = EditProfile(instance=request.user)
        return render(request, 'lesson/profile_edit.html', {'form': form})


def register_course_admin(request):
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
