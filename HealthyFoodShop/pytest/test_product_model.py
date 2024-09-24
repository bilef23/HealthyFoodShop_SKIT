import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from HealthyFoodApp.models import Product, User, Category
from decimal import Decimal


@pytest.mark.django_db
class TestProductModel:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password')

    @pytest.fixture
    def category(self):
        return Category.objects.create(name='Electronics', description='Electronic items')

    # Test valid creation
    def test_create_product_valid(self, user, category):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        product = Product.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            user=user,
            category=category,
            image=image,
            price=999.99,
            quantity=10
        )

        assert product.name == "Laptop"
        assert product.description == "A high-performance laptop."
        assert product.user == user
        assert product.category == category
        assert product.image.name.startswith('img/')
        assert product.price == 999.99
        assert product.quantity == 10

    # Test invalid creation - missing required field name
    def test_create_product_missing_name(self, user, category):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        product = Product(
            description="A high-performance laptop.",
            user=user,
            category=category,
            image=image,
            price=999.99,
            quantity=10
        )
        with pytest.raises(ValidationError):
            product.full_clean()

    # Test invalid creation - missing required field description
    def test_create_product_missing_description(self, user, category):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        product = Product(
            name="Laptop",
            user=user,
            category=category,
            image=image,
            price=999.99,
            quantity=10
        )
        with pytest.raises(ValidationError):
            product.full_clean()

    # Test invalid creation - missing required field description blank
    def test_create_product_blank_description(self, user, category):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        product = Product.objects.create(
            name="Laptop",
            description="",  # Blank but not null
            user=user,
            category=category,
            image=image,
            price=999.99,
            quantity=10
        )

        assert product.description == ""

    # Test invalid creation - missing required field price
    def test_create_product_invalid_price(self, user, category):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        product = Product(
            name="Laptop",
            description="A high-performance laptop.",
            user=user,
            category=category,
            image=image,
            price='invalid_price',
            quantity=10
        )
        with pytest.raises(ValidationError):
            product.full_clean()

    # Test valid update
    def test_update_product_valid(self, user, category):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        product = Product.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            user=user,
            category=category,
            image=image,
            price=999.99,
            quantity=10
        )

        product.name = "Gaming Laptop"
        product.price = 1299.99
        product.save()

        updated_product = Product.objects.get(code=product.code)
        assert updated_product.name == "Gaming Laptop"
        assert updated_product.price == Decimal('1299.99')

    # Test invalid update - invalid image
    def test_update_product_invalid_image(self, user, category):
        product = Product.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            user=user,
            category=category,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            price=999.99,
            quantity=10
        )

        invalid_image = SimpleUploadedFile(name='invalid_image.txt', content=b'', content_type='text/plain')
        product.image = invalid_image

        with pytest.raises(ValidationError):
            product.full_clean()

    # Test valid deletion
    def test_delete_product_valid(self, user, category):
        product = Product.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            user=user,
            category=category,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            price=999.99,
            quantity=10
        )

        id = product.code
        product.delete()

        with pytest.raises(Product.DoesNotExist):
            Product.objects.get(code=id)

    # Test invalid deletion - non-existing product
    def test_delete_non_existing_product(self):
        with pytest.raises(Product.DoesNotExist):
            Product.objects.get(code=9999).delete()

    # Test __str__ method
    def test_str_method(self,user,category):
        product = Product.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            user=user,
            category=category,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            price=999.99,
            quantity=10
        )

        assert product.__str__() == "Laptop"
