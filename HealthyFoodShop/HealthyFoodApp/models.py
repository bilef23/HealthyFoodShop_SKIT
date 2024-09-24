from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    description=models.CharField(max_length=100, null=False, blank=False)
    active=models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return self.name
class Product(models.Model):
    code=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100, null=False,blank=False)
    description=models.TextField(max_length=100, null=False, blank=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='img/')
    price=models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
    quantity=models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name
class Client(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    lastName=models.CharField(max_length=100, null=False, blank=False)
    address= models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name + " " + self.lastName

class Sale(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
    client=models.ForeignKey(Client,on_delete=models.CASCADE, null=False)
    date=models.DateField()
    quantity=models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.date