from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render
from functools import wraps

from ..models import Course


def course_required(func):
    def check_course_in_user(*args, **kwargs):
        try:
            args[0].user.courses_learn.get(
                name=kwargs.get('course_name'))
            result = func(*args, **kwargs)
            return result
        except Exception:
            print("QWEQWEQWE")
            return render(args[0], 'lesson/permission_denied.html')

    return check_course_in_user


def search_request(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        query = request.GET.get('search')
        if query is not None:
            queryset = Course.objects.annotate(
                similarity=TrigramSimilarity('name', query)
            ).filter(similarity__gt=.01).order_by('-similarity')
        else:
            queryset = None
        return view_func(request, queryset=queryset, *args, **kwargs)

    return wrapper
