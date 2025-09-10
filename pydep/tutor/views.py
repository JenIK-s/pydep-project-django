from django.shortcuts import render

from .models import FilesProject


def my_tutor(request):
    return render(request, "tutor/my_tutor.html")


def projectbox(request):
    files = FilesProject.objects.all()
    return render(request, "tutor/projectbox.html", {"files": files})
