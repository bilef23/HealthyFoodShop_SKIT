import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from HealthyFoodApp.models import Category, Product, Client
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
class TestAdmin:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password')
    @pytest.fixture
    def category(self):
        return Category.objects.create(name='Electronics', description='Electronic items')

    @pytest.fixture
    def regular_user_client(self, client):
        user = User.objects.create_user(username='testuser', password='password')
        client.login(username='testuser', password='password')
        return client
    @pytest.fixture
    def admin_client(self, client):
        user = User.objects.create_superuser(username='admin', password='testpass', email='admin@example.com')
        client.login(username='admin', password='testpass')
        return client


    # Test that a regular user is unable to delete a category in the admin panel
    def test_admin_delete_category_as_regular_user(self, regular_user_client):
        category = Category.objects.create(name="Test Category", description="Some description", active=True)

        response = regular_user_client.get(reverse('admin:HealthyFoodApp_category_delete', args=[category.id]))

        assert response.status_code == 302

        response = regular_user_client.post(reverse('admin:HealthyFoodApp_category_delete', args=[category.id]))

        assert response.status_code == 302
        assert Category.objects.filter(id=category.id).exists()

    # Test valid client listing
    @pytest.mark.django_db
    def test_admin_client_listing(self, admin_client):
        Client.objects.create(name="Test Client", lastName="Last Name")

        response = admin_client.get(reverse('admin:HealthyFoodApp_client_changelist'))

        assert response.status_code == 200
        assert 'Test Client' in str(response.content)
