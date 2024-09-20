import os
import json
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "person_service.settings")
django.setup()

from django.test.client import RequestFactory
from ..person_api.views import person_api


def test_get_all_persons():
    fact = RequestFactory()
    request = fact.get('api/v1/persons/')
    response = person_api(request)
    assert response.status_code == 200


def test_get_existing_person_by_id():
    fact = RequestFactory()
    pers_data = {'name': 'pers1',
                 'age': 22,
                 'address': 'address1',
                 'work': 'work1'}
    request = fact.post('/api/v1/persons/', data=pers_data, content_type='application/json')
    response = person_api(request)
    location = response.headers['Location']
    pers_id = int(location[location.rfind('/') + 1:])
    request = fact.get('api/v1/persons/')
    response = person_api(request, pers_id)
    assert response.status_code == 200

    request = fact.delete('/api/v1/persons/')
    person_api(request, pers_id)


def test_get_not_existing_person_by_id():
    fact = RequestFactory()
    request = fact.get('api/v1/persons/')
    response = person_api(request, -1)
    assert response.status_code == 404


def test_post_person_positive():
    fact = RequestFactory()
    pers_data = {'name': 'pers1',
                 'age': 22,
                 'address': 'address1',
                 'work': 'work1'}
    request = fact.post('/api/v1/persons/', data=pers_data, content_type='application/json')
    response = person_api(request)
    assert response.status_code == 201

    location = response.headers['Location']
    pers_id = int(location[location.rfind('/') + 1:])
    request = fact.delete('api/v1/persons/', pers_id)
    person_api(request, pers_id)


def test_post_person_invalid_data():
    fact = RequestFactory()
    pers_data = {'first_name': 'pers1'}
    request = fact.post('/api/v1/persons/', data=pers_data, content_type='application/json')
    response = person_api(request)
    assert response.status_code == 400


def delete_existing_person():
    fact = RequestFactory()
    pers_data = {'name': 'pers1',
                 'age': 22,
                 'address': 'address1',
                 'work': 'work1'}
    request = fact.post('/api/v1/persons/', data=pers_data, content_type='application/json')
    response = person_api(request)

    location = response.headers['Location']
    pers_id = int(location[location.rfind('/') + 1:])
    request = fact.delete('/api/v1/persons/')
    response = person_api(request, pers_id)
    assert response.status_code == 204


def delete_not_existing_person():
    fact = RequestFactory()
    request = fact.delete('/api/v1/persons/')
    response = person_api(request, -1)
    assert response.status_code == 204
