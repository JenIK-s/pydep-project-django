from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .serializers import (
    UsersSerializer, CourseGetSerializer, CoursePostSerializer,
    ModuleGetSerializer, ModulePostSerializer, LessonGetSerializer,
    LessonPostSerializer,
)

from users.models import CustomUser
from lesson.models import Lesson, Module, Course


class UserViewSet(ModelViewSet):
    serializer_class = UsersSerializer
    queryset = CustomUser.objects.all()


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CoursePostSerializer
        return CourseGetSerializer


class ModuleViewSet(ModelViewSet):
    queryset = Module.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ModulePostSerializer
        return ModuleGetSerializer


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return LessonPostSerializer
        return LessonGetSerializer
