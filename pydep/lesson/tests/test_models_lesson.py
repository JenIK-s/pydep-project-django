import pytest

from lesson.models import Category
from lesson.models import Lesson
from lesson.models import Module
from lesson.models import Course
from lesson.models import ModulesInCourse
from lesson.models import LessonsInModule
from lesson.models import UserLessonProgress
from users.models import CustomUser


@pytest.fixture
def category():
    return Category.objects.create(name="Тест")


@pytest.fixture
def lesson():
    return Lesson.objects.create(
        title="test",
        description="test",
    )


@pytest.fixture
def module():
    return Module.objects.create(
        title="test",
        description="test",
        image="test/test.jpg",
    )


@pytest.fixture
def course():
    return Course.objects.create(
        name="test",
        description="test",
        image="test/test.jpg",
    )


@pytest.mark.django_db
def test_category(category):
    assert category.name == "Тест"
    assert category.slug == "test"
    assert Category.objects.count() == 1
    assert str(category) == "Тест"


@pytest.mark.django_db
def test_lesson(lesson):
    assert lesson.title == "test"
    assert lesson.description == "test"
    assert Lesson.objects.count() == 1
    assert str(lesson) == "test"


@pytest.mark.django_db
def test_module(lesson, module):
    assert module.title == "test"
    assert module.description == "test"
    assert module.lessons.count() == 0
    assert Module.objects.count() == 1

    module.lessons.add(lesson)

    assert module.lessons.count() == 1
    assert module.lessons.all().first().title == "test"
    assert module.lessons.all().first().description == "test"

    assert str(module) == "test"


@pytest.mark.django_db
def test_course(module, course, category):
    assert course.name == "test"
    assert course.description == "test"
    assert course.price == 1000
    assert course.duration == 3
    assert course.level == "С нуля"
    assert course.category is None
    assert course.modules.count() == 0

    course.category = category
    course.save()
    assert course.category == category

    course.modules.add(module)
    assert course.modules.count() == 1

    assert str(course) == "test"


@pytest.mark.django_db
def test_module_in_course(module, course):
    ModulesInCourse.objects.create(
        course=course,
        module=module,
    )

    assert ModulesInCourse.objects.count() == 1
    assert ModulesInCourse.objects.all().first().module == module
    assert ModulesInCourse.objects.all().first().course == course


@pytest.mark.django_db
def test_lesson_in_module(lesson, module):
    LessonsInModule.objects.create(
        lesson=lesson,
        module=module,
    )

    assert LessonsInModule.objects.count() == 1
    assert LessonsInModule.objects.all().first().lesson == lesson
    assert LessonsInModule.objects.all().first().module == module


@pytest.mark.django_db
def test_user_lesson_progress(lesson, module, course):
    user = CustomUser.objects.create_user(username="test_case", password="jer214TFG2")

    module.lessons.add(lesson)
    course.modules.add(module)

    UserLessonProgress.objects.create(user=user, lesson=lesson, module=module, course=course)

    progress = UserLessonProgress.objects.all().first()
    assert UserLessonProgress.objects.count() == 1
    assert progress.user == user
    assert progress.lesson == lesson
    assert progress.module == module
    assert progress.course == course
    assert progress.current == False
    assert progress.completed == False

    assert str(progress) == f"{user} {lesson} {False}"
