import pytest
from django.urls import reverse

from lesson.models import Category
from lesson.models import Course
from lesson.models import Lesson
from lesson.models import Module
from users.models import CustomUser


@pytest.fixture
def course():
    lesson = Lesson.objects.create(title="Test", description="Test")
    module = Module.objects.create(
        title="Test",
        description="Test",
        image="test/test.jpg"
    )
    category = Category.objects.create(name="Programming")
    module.lessons.add(lesson)
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
    return CustomUser.objects.create_user(
        username="test_case",
        password="jer214TFG2"
    )


class TestUrls:
    urls_status = {
        reverse("lesson:index"): (200, 200),
        reverse("lesson:profile"): (302, 200),
        reverse("lesson:profile_edit"): (302, 200),
        reverse("lesson:courses"): (200, 200),
    }

    @pytest.mark.django_db
    def test_urls_none_auth(self, client, course):
        for url in self.urls_status:
            response = client.get(url)
            assert response.status_code == self.urls_status.get(url)[0]

    @pytest.mark.django_db
    def test_urls_auth(self, client):
        user = CustomUser.objects.create_user(
            username='test',
            password='Gnusmas4'
        )
        client.force_login(user)
        for url in self.urls_status:
            response = client.get(url)
            assert response.status_code == self.urls_status.get(url)[1]

    @pytest.mark.django_db
    def test_param_urls_none_auth(self, client, course):
        url = reverse(
            "lesson:course_detail",
            kwargs={"course_name": course.name}
        )
        resp = client.get(url, follow=False)
        assert resp.status_code in (301, 302)
        login_url = reverse('users:signin')
        assert login_url in resp.url

        url = reverse("lesson:category", kwargs={"slug": course.category.slug})
        assert client.get(url).status_code == 200

        url = reverse("lesson:module_detail", kwargs={
            "course_name": course.name,
            "module_name": course.modules.first().title,
        })
        resp = client.get(url, follow=False)
        assert resp.status_code in (301, 302)
        login_url = reverse('users:signin')
        assert login_url in resp.url

        url = reverse("lesson:lesson_detail", kwargs={
            "course_name": course.name,
            "module_name": course.modules.first().title,
            "lesson_name": course.modules.first().lessons.first().title,
        })
        resp = client.get(url, follow=False)
        assert resp.status_code in (301, 302)
        login_url = reverse('users:signin')
        assert login_url in resp.url

    @pytest.mark.django_db
    def test_param_urls_auth(self, client, course, user):
        client.force_login(user)

        url = reverse(
            "lesson:course_detail",
            kwargs={"course_name": course.name}
        )
        assert client.get(url).status_code == 200

        url = reverse("lesson:category", kwargs={"slug": course.category.slug})
        assert client.get(url).status_code == 200

        url = reverse("lesson:module_detail", kwargs={
            "course_name": course.name,
            "module_name": course.modules.first().title,
        })
        assert client.get(url).status_code == 200

        url = reverse("lesson:lesson_detail", kwargs={
            "course_name": course.name,
            "module_name": course.modules.first().title,
            "lesson_name": course.modules.first().lessons.first().title,
        })
        assert client.get(url).status_code == 200
