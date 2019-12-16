from django.db import models
from login_app.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Purchase(models.Model):
    item_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, related_name='purchases', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Challenge(models.Model):
    name = models.CharField(max_length=255)
    purchase_max = models.DecimalField(max_digits=9, decimal_places=2)
    dollar_max = models.DecimalField(max_digits=9, decimal_places=2)
    users = models.ManyToManyField(User, related_name='challenges')
    categories = models.ManyToManyField(Category, related_name='challenges')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
