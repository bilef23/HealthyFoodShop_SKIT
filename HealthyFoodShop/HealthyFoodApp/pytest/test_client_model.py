import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from HealthyFoodApp.models import Client

@pytest.mark.django_db
class TestClientModel:

    @pytest.fixture
    def client(self):
        return Client.objects.create(
            name="John",
            lastName="Doe",
            address="123 Main St",
            email="johndoe@example.com"
        )
    # Valid client creation
    def test_create_client_valid(self, client):

        assert client.id is not None
        assert client.name == "John"
        assert client.lastName == "Doe"
        assert client.address == "123 Main St"
        assert client.email == "johndoe@example.com"

    # Test invalid client creation - Missing required field name
    def test_create_client_missing_name(self):
        with pytest.raises(ValidationError):
            client=Client(
                lastName="Doe",
                address="123 Main St",
                email="johndoe@example.com"
            )
            client.full_clean()

    # Test invalid client creation - invalid email format
    def test_create_client_invalid_email(self):
        with pytest.raises(ValidationError):
            client = Client(
                name="John",
                lastName="Doe",
                address="123 Main St",
                email="invalidemail"
            )
            client.full_clean()


    # Test valid client update
    def test_update_client_valid(self, client):
        client.name = "Jane"
        client.email = "janedoe@example.com"
        client.save()

        updated_client = Client.objects.get(id=client.id)
        assert updated_client.name == "Jane"
        assert updated_client.email == "janedoe@example.com"

    # Test invalid client update - invalid email format
    def test_update_client_invalid_email(self, client):

        client.email = "invalidemail"
        with pytest.raises(ValidationError):
            client.full_clean()

    # Test valid client deletion
    def test_delete_client_valid(self, client):

        client_id = client.id
        client.delete()

        with pytest.raises(Client.DoesNotExist):
            Client.objects.get(id=client_id)

    # Test invalid client deletion - Non-existing client
    def test_delete_non_existing_client(self):
        with pytest.raises(Client.DoesNotExist):
            Client.objects.get(id=999999).delete()

    # Test client __str__ method
    def test_str_method(self, client):
        assert client.__str__() == "John Doe"
