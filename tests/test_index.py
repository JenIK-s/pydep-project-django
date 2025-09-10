import pytest


def test_in(user_client):
    response = user_client.get("/")
    assert response.status_code == 201
