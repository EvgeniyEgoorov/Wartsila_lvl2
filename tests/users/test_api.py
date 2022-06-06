import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from users.models import Profile


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def profiles_factory():
    def factory(*args, **kwargs):
        return baker.make(Profile, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_profiles(client, profiles_factory):
    profiles = profiles_factory(_quantity=10)
    response = client.get('/profiles/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(profiles)
    for i, profile in enumerate(data):
        assert profile['bio'] == profiles[i].bio


@pytest.mark.django_db
def test_post_profile(client):
    count = Profile.objects.count()
    inputs = {
        'login': 'login',
        'password': 'password',
        'bio': 'Hello from here!'
    }
    response = client.post('/profiles/', inputs)
    assert response.status_code == 201
    assert Profile.objects.count() == count + 1

