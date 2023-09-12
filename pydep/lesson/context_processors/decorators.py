from django.shortcuts import render


def course_required(func):
    def check_course_in_user(*args, **kwargs):
        try:
            learn_course = args[0].user.courses_learn.get(name=kwargs.get('course_name'))
            result = func(*args, **kwargs)
            return result
        except:
            return render(args[0], 'lesson/register_course.html')
    return check_course_in_user
