from django.shortcuts import render


def index(request):
    return render(request, 'lesson/index.html')


def courses_list(request):
    return render(request, 'lesson/courses_list.html')
