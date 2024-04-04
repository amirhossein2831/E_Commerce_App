import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Collection


@pytest.fixture
def get_collections(api_client):
    def do_get_collections(pk=None):
        if pk is not None:
            return api_client.get(f'/store/collections/{pk}/')
        else:
            return api_client.get('/store/collections/')

    return do_get_collections


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)

    return do_create_collection


class TestQueryCollection:
    def test_if_user_is_anonymous_return_401(self, get_collections):
        response = get_collections()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_if_user_is_authenticate_return_200_list(self, authenticated_client, get_collections):
        authenticated_client()
        collections_number = 4
        baker.make(Collection, _quantity=collections_number)

        response = get_collections()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == collections_number

    @pytest.mark.django_db
    def test_if_user_is_authenticate_return_200_detail(self, authenticated_client, get_collections):
        authenticated_client()
        collection = baker.make(Collection)

        response = get_collections(pk=collection.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == collection.id


class TestCommandCollection:
    def test_if_user_is_anonymous_return_401(self, api_client, create_collection):
        response = create_collection({'title': 'test'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticated_client, create_collection):
        authenticated_client()

        response = create_collection({'title': 'test'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_if_data_is_invalid_return_400(self, authenticated_client, create_collection):
        authenticated_client(is_staff=True)

        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    @pytest.mark.django_db
    def test_create_if_data_is_valid_return_200(self, authenticated_client, create_collection):
        authenticated_client(is_staff=True)

        response = create_collection({'title': 'test'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    @pytest.mark.django_db
    def test_update_if_user_is_admin_return_204(self, authenticated_client, api_client):
        authenticated_client(is_staff=True)
        updated_title = 'updated'
        collection = baker.make(Collection)

        response = api_client.patch(f'/store/collections/{collection.id}/', {'title': updated_title})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == updated_title

    @pytest.mark.django_db
    def test_delete_if_user_is_admin_return_204(self, authenticated_client, api_client):
        authenticated_client(is_staff=True)
        collection = baker.make(Collection)

        response = api_client.delete(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Collection.objects.filter(pk=collection.id).exists()
