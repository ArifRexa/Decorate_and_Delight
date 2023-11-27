from django.db import models
from accounts.models import CustomUser
import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/category_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/category_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True, default="")
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    description = models.CharField(max_length=350, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_stock = models.BooleanField(default=True)
    stock_amount = models.IntegerField(default=1)
    ratings = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    created_date = models.DateTimeField(default=timezone.now, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# class ReviewRatings(models.Model):


class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} - {self.user}"
