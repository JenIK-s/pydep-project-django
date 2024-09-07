from ..models import Course


def prog_langs(request):
    return {
        'prog_langs': set(
            course.programming_language for course in Course.objects.all()
        )
    }
