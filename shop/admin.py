from django.contrib import admin
from .models import Product, Contact, Order, OrderUpdate, Cart, PromoCode, TempAmount, Extra_fields, default_image
# Register your models here.
admin.site.register((Product, Contact, Order, OrderUpdate, Cart, PromoCode, TempAmount))
admin.site.register(Extra_fields)
admin.site.register(default_image)