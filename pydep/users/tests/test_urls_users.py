import pytest
from django.urls import reverse

from users.models import CustomUser


@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        username="test_case",
        password="jer214TFG2"
    )


class TestSignIn:
    @pytest.mark.django_db
    def test_signin_get(self, client):
        url = reverse("users:signin")
        response = client.get(url)

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_signin_post_success(self, client, user):
        url = reverse("users:signin")
        response = client.post(
            url,
            data={"username": "test_case", "password": "jer214TFG2"}
        )

        assert response.status_code in (301, 302)
        assert reverse("lesson:profile") in response.url

    @pytest.mark.django_db
    def test_signin_redirect_if_already_authenticated(self, client, user):
        client.login(username="test_case", password="jer214TFG2")
        url = reverse("users:signin")
        response = client.get(url)

        assert response.status_code in (301, 302)
        assert reverse("lesson:profile") in response.url

    @pytest.mark.django_db
    def test_signin_post_none_valid(self, client):
        url = reverse("users:signin")
        response = client.post(
            url,
            data={"username": "test_case", "password": "123"}
        )

        assert response.status_code == 200


class SignUp:
    @pytest.mark.django_db
    def test_signup_get(self, client):
        url = reverse("users:signup")
        response = client.get(url)

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_signup_post_success(self, client):
        url = reverse("users:signup")
        payload = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "new@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        response = client.post(url, data=payload)

        assert response.status_code in (301, 302)
        assert reverse("users:signin") in response.url
