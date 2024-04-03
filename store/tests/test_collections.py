import pytest
from django.contrib.auth.models import User
from rest_framework import status


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)

    return do_create_collection


class TestCreateCollection:
    def test_if_user_is_anonymous_return_401(self, api_client, create_collection):
        response = create_collection({'title': 'test'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticated_client, create_collection):
        authenticated_client()

        response = create_collection({'title': 'test'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, authenticated_client, create_collection):
        authenticated_client(is_staff=True)

        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_200(self, authenticated_client, create_collection, db):
        authenticated_client(is_staff=True)

        response = create_collection({'title': 'test'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
