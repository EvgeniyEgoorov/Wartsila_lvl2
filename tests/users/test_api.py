import pytest
from model_bakery import baker
from rest_framework.test import APIClient
import json

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
def test_get_profiles_list(client, profiles_factory):
    profiles = profiles_factory(_quantity=10)
    response = client.get('/profiles/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(profiles)
    for i, profile in enumerate(data):
        assert profile['bio'] == profiles[i].bio


@pytest.mark.django_db
def test_get_profile_by_id(client):
    profile = Profile.objects.create_user(
        username='my_login',
        password='my_password',
    )
    response = client.get(f'/profiles/{profile.id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['login'] == 'my_login'


@pytest.mark.django_db
def test_filter_by_multiple_fields(client, profiles_factory):
    profiles_factory(_quantity=10)
    profile = Profile.objects.create_user(
        username='my_login',
        password='my_password',
        city='Moscow'
    )
    response = client.get(f'/profiles/?login={profile.login}&city={profile.city}')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['login'] == 'my_login'
    assert data[0]['city'] == 'Moscow'


@pytest.mark.django_db
def test_post_new_profile(client):
    count = Profile.objects.count()
    inputs = {
        'login': 'my_login',
        'password': 'my_password',
    }
    response = client.post('/profiles/', inputs)
    assert response.status_code == 201
    assert Profile.objects.count() == count + 1


@pytest.mark.django_db
def test_patch_profile(client):
    profile = Profile.objects.create_user(
        username='login',
        password='my_password'
    )
    data = {'bio': 'Hello from here!'}
    header = {'HTTP_AUTHORIZATION': f'Token {profile.auth_token.key}'}
    response = client.patch(
        f'/profiles/{profile.id}/', content_type='application/json', data=json.dumps(data), follow=True, **header)
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data['bio'] == data['bio']


@pytest.mark.django_db
def test_delete_profile(client):
    profile = Profile.objects.create_user(
        username='login',
        password='password',
    )
    header = {'HTTP_AUTHORIZATION': f'Token {profile.auth_token.key}'}
    response = client.delete(f'/profiles/{profile.id}/', follow=True, **header)
    assert response.status_code == 204
    response2 = client.get('/profiles/')
    data = response2.json()
    assert len(data) == 0
