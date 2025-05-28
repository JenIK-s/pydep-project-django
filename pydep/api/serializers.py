from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from users.models import CustomUser
from lesson.models import Lesson, Module, Course

from lesson.models import LessonsInModule


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'password')


class LessonGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class ModuleGetSerializer(serializers.ModelSerializer):
    lessons = LessonGetSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = "__all__"


class ModulePostSerializer(serializers.ModelSerializer):
    lessons = serializers.ListField()

    class Meta:
        model = Module
        fields = ("title", "description", "lessons")

    def create(self, validated_data):
        lessons_data = validated_data.pop("lessons")
        module = Module.objects.create(**validated_data)
        for i, elem in enumerate(lessons_data):
            if isinstance(elem, int):
                lesson = Lesson.objects.get(id=elem)
            elif isinstance(elem, dict):
                lesson = Lesson.objects.create(**elem)
            else:
                raise serializers.ValidationError("int or dict")
            LessonsInModule.objects.create(module=module, lesson=lesson)

        return module

    def update(self, module, validated_data):
        return None


class CourseGetSerializer(serializers.ModelSerializer):
    modules = ModuleGetSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class CoursePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
