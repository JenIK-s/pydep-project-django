import pytest
from django.urls import reverse
from users.models import CustomUser


@pytest.mark.django_db
def test_index_page(client):
    url = reverse('lesson:index')
    response = client.get(url)

    assert response.status_code == 200
