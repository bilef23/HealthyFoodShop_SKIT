import pytest
from django.core.exceptions import ValidationError
from HealthyFoodApp.models import Category

@pytest.mark.django_db
class TestCategoryModel:

    # Test valid category creation
    def test_create_valid_category(self):
        category = Category.objects.create(name="Fruits", description="Fresh fruits", active=True)

        assert category.name == "Fruits"
        assert category.description == "Fresh fruits"
        assert category.active is True

    # Test invalid category creation - empty name
    def test_create_category_invalid_name(self):

        with pytest.raises(ValidationError):
            category = Category(name="", description="Invalid category", active=True)
            category.full_clean()


    # Test invalid category creation - name is None
    def test_create_category_name_none(self):
        with pytest.raises(ValidationError):
            category = Category(name=None, description="Invalid", active=True)
            category.full_clean()

    # Test invalid category creation - empty description
    def test_create_category_invalid_description(self):
        with pytest.raises(ValidationError):
            category = Category(name="Invalid", description="", active=True)
            category.full_clean()

    # Test invalid category creation - description is None
    def test_create_category_description_none(self):
        with pytest.raises(ValidationError):
            category = Category(name="Invalid", description=None, active=True)
            category.full_clean()

    # Test valid category update (edit)
    def test_edit_valid_category(self):
        category = Category.objects.create(
            name="Fruits",
            description="Seasonal fruits",
            active=True
        )
        category.name = "Fresh Fruits"
        category.save()
        updated_category = Category.objects.get(pk=category.pk)
        assert updated_category.name == "Fresh Fruits"

    def test_edit_category(self):
        category = Category.objects.create(name="Vegetables", description="Fresh vegetables", active=True)

        category.name = "Green Vegetables"
        category.save()

        updated_category = Category.objects.get(id=category.id)
        assert updated_category.name == "Green Vegetables"
        assert updated_category.description == "Fresh vegetables"

    # Test category __str__ method
    def test_str_method(self):
        category = Category.objects.create(name="Fruits", description="Fresh vegetables", active=True)

        assert category.__str__() == "Fruits"

    # Test that a category is successfully deleted from the database
    def test_delete_category(self):
        category = Category.objects.create(name="Dairy", description="Milk and cheese", active=True)

        category_id = category.id
        category.delete()

        with pytest.raises(Category.DoesNotExist):
            Category.objects.get(id=category_id)


