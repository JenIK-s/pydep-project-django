import pytest
from django.urls import reverse

from lesson.models import Lesson
from lesson.models import Module
from lesson.models import Course
from users.models import CustomUser


@pytest.fixture
def course(db):
    lesson = Lesson.objects.create(title="Test", description="Test")
    module = Module.objects.create(title="Test", description="Test", image="test/test.jpg")
    module.lessons.add(lesson)
    module.save()
    course = Course.objects.create(
        name="Test",
        description="Test",
        image="test/test.jpg",
        programming_language="Python",
    )
    course.modules.add(module)
    course.save()


class TestUrls:
    urls_status = {
        reverse("lesson:index"): (200, 200),
        reverse("lesson:profile"): (302, 200),
        reverse("lesson:profile_edit"): (302, 200),
        reverse("lesson:courses"): (200, 200),
        reverse("lesson:create_lesson"): (302, 200),
        # reverse("lesson:course_detail"): 200,
        # reverse("lesson:category"): 200,
        # reverse("lesson:module_detail"): 200,
        # reverse("lesson:lesson_detail"): 200,
    }


    def test_urls_none_auth(self, client, course):
        for url in self.urls_status:
            response = client.get(url)
            assert response.status_code == self.urls_status.get(url)[0]

    @pytest.mark.django_db
    def test_urls_auth(self, client):
        user = CustomUser.objects.create_user(username='test', password='Gnusmas4')
        client.force_login(user)
        for url in self.urls_status:
            response = client.get(url)
            assert response.status_code == self.urls_status.get(url)[1]

