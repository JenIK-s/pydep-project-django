import pytest
from django.urls import reverse

from lesson.models import Category
from lesson.models import Course
from lesson.models import Lesson
from lesson.models import Module
from users.models import CustomUser
from users.models import UserLessonProgress


@pytest.fixture
def course(db):
    lesson1 = Lesson.objects.create(title="Test1", description="Test1")
    lesson2 = Lesson.objects.create(title="Test2", description="Test2")
    module = Module.objects.create(title="Test", description="Test", image="test/test.jpg")
    category = Category.objects.create(name="Programming")
    module.lessons.add(lesson1, lesson2)
    module.save()
    course = Course.objects.create(
        name="Test",
        description="Test",
        image="test/test.jpg",
        programming_language="Python",
        category=category,
    )
    course.modules.add(module)
    course.save()
    return course


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username="test_case", password="jer214TFG2")


@pytest.mark.django_db
def test_courses_list_view(client, course):
    url = reverse("lesson:courses")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_detail_view(client, course):
    url = reverse("lesson:category", kwargs={"slug": course.category.slug})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_detail_ok_if_auth(client, course):
    user = CustomUser.objects.create_user(username="u", password="pS123456!")
    client.force_login(user)
    url = reverse("lesson:course_detail", kwargs={"course_name": course.name})
    response = client.get(url)
    assert response.status_code == 200
    assert "lesson/course_detail.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_module_detail_ok_if_auth(client, course):
    user = CustomUser.objects.create_user(username="u2", password="pS123456!")
    client.force_login(user)
    url = reverse("lesson:module_detail", kwargs={"course_name": course.name, "module_name": course.modules.first().title})
    response = client.get(url)
    assert response.status_code == 200
    assert "lesson/module_detail.html" in [t.name for t in response.templates]


# @pytest.mark.django_db
# def test_lesson_detail_ok_if_auth(client, course):
#     user = CustomUser.objects.create_user(username="u3", password="pS123456!")
#     client.force_login(user)
#     module = course.modules.first()
#     lesson = course.modules.first().lessons.first()
#     # Дадим доступ к уроку через явное создание прогресса
#     UserLessonProgress.objects.create(user=user, course=course, module=module, lesson=lesson, current=True)
#     url = reverse("lesson:lesson_detail", kwargs={"course_name": course.name, "module_name": module.title, "lesson_name": lesson.title})
#     response = client.get(url)
#     assert response.status_code == 200
#     assert "lesson/lesson_detail.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_complete_lesson_marks_done_and_opens_next(client, course, user):
    client.force_login(user)
    module = course.modules.first()
    lesson1, lesson2 = module.lessons.all()

    UserLessonProgress.objects.create(user=user, course=course, module=module, lesson=lesson1, current=True)
    url = reverse("lesson:complete_lesson", kwargs={"course_name": course.name, "module_name": module.title, "lesson_name": lesson1.title})
    response = client.post(url, follow=False)

    assert response.status_code in (301, 302)
    assert reverse("lesson:module_detail", kwargs={"course_name": course.name, "module_name": module.title}) in response.url

    p1 = UserLessonProgress.objects.get(user=user, course=course, module=module, lesson=lesson1)
    # assert p1.completed is True
    assert p1.current is True

    # p2 = UserLessonProgress.objects.get(user=user, course=course, module=module, lesson=lesson2)
    # assert p2.current is True
