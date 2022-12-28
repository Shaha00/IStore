from django.db import models


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=55)


class Product(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateField(auto_now=True)
    modified_date = models.DateField(auto_now_add=True)
    rate = models.FloatField()
    categories = models.ManyToManyField(Category)
    reviewtable = models.BooleanField(default=True)


class Review(models.Model):
    post = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="reviews")
    text = models.TextField()
    created_date = models.DateField(auto_now=True)
