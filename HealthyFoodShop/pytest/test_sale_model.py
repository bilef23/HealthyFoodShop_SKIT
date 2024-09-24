import pytest
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from HealthyFoodApp.models import Product, Client, Sale, Category
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

@pytest.mark.django_db
class TestSaleModel:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password')

    @pytest.fixture
    def category(self):
        return Category.objects.create(name='Electronics', description='Electronic items')

    @pytest.fixture
    def setup_data(self, user, category):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        product = Product.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            user=user,
            category=category,
            image=image,
            price=Decimal('999.99'),
            quantity=10
        )

        client = Client.objects.create(
            name="John",
            lastName="Doe",
            address="123 Main St",
            email="johndoe@example.com"
        )

        return product, client

    # Test valid sale creation
    def test_create_sale_valid(self, setup_data):
        product, client = setup_data

        sale = Sale.objects.create(
            product=product,
            client=client,
            date=date.today(),
            quantity=2
        )

        assert sale.product == product
        assert sale.client == client
        assert sale.date == date.today()
        assert sale.quantity == 2

    # Test invalid sale creation - missing required field product
    def test_create_sale_missing_product(self, setup_data):
        _, client = setup_data

        with pytest.raises(IntegrityError):
            Sale.objects.create(
                product=None,
                client=client,
                date=date.today(),
                quantity=2
            )

    # Test invalid sale creation - missing required field client
    def test_create_sale_missing_client(self, setup_data):
        product, _ = setup_data

        with pytest.raises(IntegrityError):
            Sale.objects.create(
                product=product,
                client=None,
                date=date.today(),
                quantity=2
            )

    # Test invalid sale creation - missing required field date
    def test_create_sale_missing_date(self, setup_data):
        product, client = setup_data

        with pytest.raises(IntegrityError):
            Sale.objects.create(
                product=product,
                client=client,
                date=None,
                quantity=2
            )

    # Test invalid sale creation - missing required field quantity
    def test_create_sale_missing_quantity(self, setup_data):
        product, client = setup_data

        with pytest.raises(IntegrityError):
            Sale.objects.create(
                product=product,
                client=client,
                date=date.today(),
                quantity=None
            )
    # Test valid sale update
    def test_update_sale_valid(self, setup_data):
        product, client = setup_data

        sale = Sale.objects.create(
            product=product,
            client=client,
            date=date.today(),
            quantity=2
        )

        sale.quantity = 5
        sale.save()

        updated_sale = Sale.objects.get(id=sale.id)
        assert updated_sale.quantity == 5

    #Test valid sale deletion
    def test_delete_sale_valid(self, setup_data):
        product, client = setup_data

        sale = Sale.objects.create(
            product=product,
            client=client,
            date=date.today(),
            quantity=2
        )

        sale_id = sale.id
        sale.delete()

        with pytest.raises(Sale.DoesNotExist):
            Sale.objects.get(id=sale_id)

    # Test __str__ method
    def test_str_method(self,setup_data):
        product, client = setup_data
        sale = Sale.objects.create(
            product=product,
            client=client,
            date=date.today(),
            quantity=2
        )

        assert sale.__str__() == date.today()
