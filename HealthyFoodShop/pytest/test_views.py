import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from HealthyFoodApp.models import Category, Product
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestViews:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='testpass')
    @pytest.fixture
    def category(self):
        return Category.objects.create(name='Electronics', description='Electronic items')

    # Test valid out_of_stock view
    def test_out_of_stock_valid(self, client, category, user):
        client.login(username='testuser', password='testpass')

        image_path = '/Users/biledimitrova/Downloads/test.jpg'
        with open(image_path, 'rb') as img_file:
            image_file = SimpleUploadedFile(img_file.name, img_file.read(), content_type='image/jpeg')

            response = client.post(reverse('out_of_stock'), {
                'name': 'Test Product',
                'description': 'This is a test product.',
                'category': category.id,
                'image': image_file,
                'price': 99.99,
                'quantity': 10,
            })

        assert response.status_code == 200
        assert Product.objects.filter(name='Test Product').exists()

    # Test view out_of_stock invalid - blank name
    @pytest.mark.django_db
    def test_out_of_stock_invalid(self, client, user):

        client.login(username='testuser', password='testpass')
        category = Category.objects.create(name="Test Category")

        response = client.post(reverse('out_of_stock'), {
            'name': '',
            'description': 'This product has no name.',
            'category': category.id,
            'price': 99.99,
            'quantity': 10,
        })

        assert response.status_code == 200
        assert not Product.objects.filter(name='').exists()

    # Test view out of stock when unathenticated
    @pytest.mark.django_db
    def test_out_of_stock_unauthenticated(self, client):
        category = Category.objects.create(name="Test Category")

        response = client.post(reverse('out_of_stock'), {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'category': category.id,
            'price': 99.99,
            'quantity': 10,
        })

        assert response.status_code == 302

    # Test that the out_of_stock view displays correctly when there are no products
    @pytest.mark.django_db
    def test_out_of_stock_no_products(self, client, user):

        client.login(username='testuser', password='testpass')

        response = client.get(reverse('out_of_stock'))

        assert response.status_code == 200
        assert len(response.context['products']) == 0

    # Test that the index view displays the correct categories
    @pytest.mark.django_db
    def test_index_view(self, client):

        Category.objects.create(name="Category 1")
        Category.objects.create(name="Category 2")

        response = client.get(reverse('index'))

        assert response.status_code == 200
        assert 'index.html' in [t.name for t in response.templates]
        assert 'categories' in response.context
        assert len(response.context['categories']) == 2
        assert response.context['categories'][0].name == "Category 1"
        assert response.context['categories'][1].name == "Category 2"
