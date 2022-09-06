from pyexpat import model
from typing_extensions import Required
from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Extra_fields(AbstractUser):
    image = models.ImageField(upload_to='shop/images/', default='')

class default_image(models.Model):
    image = models.ImageField(upload_to = 'shop/images')

class Product(models.Model):
    category = models.CharField(max_length=100, default='')
    sub_category = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='shop/images', default='')
    price = models.FloatField()
    discount = models.FloatField(default='')
    description = models.TextField(max_length=5000, default='')

    def __str__(self):
        return self.name[0:60]  


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=5000)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    allitems = models.TextField(max_length=1000)
    payment_status = models.BooleanField()
    amount = models.FloatField()
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    address_line1 = models.TextField(max_length=200)
    address_line2 = models.TextField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    zip_code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.name

UPDATE_CHOICES = (
    ("Your order has been successfully placed.", "Your order has been successfully placed."),
    ("Your order has been picked by courier.", "Your order has been picked by courier."),
    ("Your order reached at ", "Your order reached at "),
    ("Your order has been successfully delivered.", "Your order has been successfully delivered.")
)

class OrderUpdate(models.Model):
    order_Id = models.IntegerField()
    payment_status = models.BooleanField()
    update_choice = models.CharField(
        max_length=500,
        choices = UPDATE_CHOICES,
        default = 'Your order has been successfully placed.'
        )
    update_desc = models.CharField(max_length=200, blank=True, default='')
    timestamp = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.order_Id)

class Cart(models.Model):
    qty = models.IntegerField(default=1)
    price = models.FloatField()
    # promo_code = models.CharField(max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class PromoCode(models.Model):
    promo_code = models.CharField(max_length=10)
    promo_amount = models.FloatField()

    def __str__(self):
        return self.promo_code

class TempAmount(models.Model):
    temp_amt = models.FloatField()

    def __str__(self):
        return str(self.temp_amt)