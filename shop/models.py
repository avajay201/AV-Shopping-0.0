from pyexpat import model
from statistics import multimode
from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from sqlalchemy import true
# Create your models here.

class Extra_fields(AbstractUser):
    image = models.ImageField(upload_to='shop/images/', default='')

class default_image(models.Model):
    image = models.ImageField(upload_to = 'shop/images')

UPDATE_CHOICES_1 = (
    ("In Stock", "In Stock"),
    ("Not In Stock", "Not In Stock")
)
class Product(models.Model):
    category = models.CharField(max_length=100, default='')
    sub_category = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='shop/images', default='')
    price = models.FloatField()
    availibility = models.CharField(
        max_length=200,
        choices = UPDATE_CHOICES_1,
        default = 'In Stock'
        )
    discount = models.FloatField(default='')
    description = models.TextField(max_length=5000, default='')
    brand = models.CharField(max_length=300)
    model_name = models.CharField(max_length=300)
    manufacturer = models.CharField(max_length=300)
    country_of_origin = models.CharField(max_length=300)
    item_weight = models.CharField(max_length=300)
    os = models.CharField(max_length=300)
    color = models.CharField(max_length=300)
    network_service_provider = models.CharField(max_length=300)
    cellular_technology = models.CharField(max_length=300)
    whats_in_the_box = models.CharField(max_length=300)
    proccessor = models.CharField(max_length=300)
    ram = models.CharField(max_length=300)
    storage = models.CharField(max_length=300)
    fingerprint_sensor = models.CharField(max_length=300)
    product_dimensions = models.CharField(max_length=300)
    battery = models.CharField(max_length=300)
    connectivity_technologies = models.CharField(max_length=300)
    gps = models.CharField(max_length=300)
    display_technology = models.CharField(max_length=300)
    camera_features = models.CharField(max_length=300)
    audio_jack = models.CharField(max_length=300)
    special_features = models.CharField(max_length=300)

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
    items_id = models.TextField(max_length=500)
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