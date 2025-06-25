from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Course, ModulesInCourse, Module, Lesson, Category, UserLessonProgress, ProjectDocument
from .forms import RegisterCourseForm, EditProfile, CreateLessonForm
from .context_processors.bot import send_message
from .context_processors.decorators import course_required, search_request
from users.models import CancelledLesson, RegisterCourse, Schedule
import os
import calendar
from datetime import datetime


def get_weekday(day):
    year = datetime.today().year
    month = datetime.today().month
    date_string = f"{year}-{month:02d}-{day:02d}"
    date = datetime.strptime(date_string, "%Y-%m-%d")
    weekday_name = date.strftime("%A")

    return weekday_name


def index(request):
    return render(request, 'lesson/index.html')


def category_detail(request, slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=slug)
    courses = Course.objects.filter(category=category)
    return render(request, "lesson/courses_list.html", {"courses": courses, "categories": categories, "category": category})


@search_request
def courses_list(request, queryset=None):
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

    # course = Course.objects.get(name=course_name)
    # modules_user = Module.objects.filter(course=course)
    # user_modules = []
    # for module in modules_user:
    #     lessons = module.lessons.all()
    #     total_lessons = lessons.count()
    #
        # completed_lessons = UserLessonProgress.objects.filter(
        #     user=request.user,
        #     lesson__in=lessons,
        #     completed=True
        # )

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
    module = Module.objects.get(title=module_name)
    lessons_module = module.lessons.all()
    completed_lessons = UserLessonProgress.objects.filter(
        user=request.user,
        lesson__in=lessons_module,
        completed=True
    ).values_list('lesson', flat=True)

    # Если в модуле не открыт первый урок, назначаем его текущим
    if module.lessons.all()[0].id not in UserLessonProgress.objects.filter(user=request.user).values_list("lesson_id", flat=True):
        UserLessonProgress.objects.create(
            user=request.user,
            lesson=module.lessons.all()[0],
            current=True
        )

    print(completed_lessons)
    lessons = []
    current_found = False
    for lesson in lessons_module:
        is_completed = lesson.id in completed_lessons
        is_current = False

        if not is_completed and not current_found:
            is_current = True
            current_found = True

        lessons.append({
            'lesson': lesson,
            'is_completed': is_completed,
            'is_current': is_current,
        })
    print(lessons)
    # module = Module.objects.get(title=module_name)
    # lessons = module.lessons.all()

    context = {
        'lessons': lessons,
        'course_name': course_name,
        'module_name': module_name
    }
    return render(request, 'lesson/module_detail.html', context)


@login_required
def complete_lesson(request, course_name, module_name, lesson_name):
    lesson = Lesson.objects.get(title=lesson_name)

    # Отметить текущий как завершённый
    progress, created = UserLessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    progress.completed = True
    progress.current = False
    progress.save()

    # Найти следующий урок
    next_lesson = None
    module = Module.objects.get(title=module_name)
    module_lessons = module.lessons.all()
    # Получаем следующий непройденный урок в модуле
    for i in range(len(module_lessons)):
        try:
            print("TRY")

            if not UserLessonProgress.objects.get(user=request.user, lesson=module_lessons[i]).completed and module_lessons[i] != lesson:
                print("IF")
                next_lesson = module_lessons[i]
                print(next_lesson)
                break
        except:
            print("EXCEPT")
            next_lesson = module_lessons[i]
            print(next_lesson)
            break
        # if module_lessons[i] == lesson and i < len(module_lessons) - 1:
        #     next_lesson = module_lessons[i + 1]
        #     if UserLessonProgress.objects.get(lesson=next_lesson).completed:
        #         continue
        #     break
    print(">>>", next_lesson)

    # next_lesson = Lesson.objects.filter(
    #     module=lesson.module,
    #     order__gt=lesson.order
    # ).order_by('order').first()

    if next_lesson:
        # Убедиться, что у следующего урока есть progress-объект
        next_progress, created = UserLessonProgress.objects.get_or_create(
            user=request.user,
            lesson=next_lesson
        )
        if not next_progress.completed:
            next_progress.current = True
            next_progress.save()

    return redirect('lesson:module_detail', course_name=course_name, module_name=module_name)


@login_required
def profile(request):
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

def projects(request, name):
    project = get_object_or_404(ProjectDocument, name=name)
    with project.file.open('r') as f:
        html_content = f.read()
    return HttpResponse(html_content)
