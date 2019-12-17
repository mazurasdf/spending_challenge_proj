from django.db import models
from login_app.models import User

class Purchase_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['item']) < 1:
            errors['item'] = 'Item name is required'
        try:
            float(post_data['amount'])
        except:
            errors['amount'] = 'Must enter valid dollar amount'
        if len(post_data['location']) < 1:
            errors['location'] = 'Location name is required'
        return errors

class Category_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['category']) < 1:
            errors['category'] = 'Must include a category'
        # if category doesn't exist then make a new one
        try:
            Category.objects.get(name=post_data['category'])
        except:
            Category.objects.create(name=post_data['category'])
        return errors

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Category_Manager()

class Purchase(models.Model):
    item_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, related_name='purchases', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Purchase_Manager()

class Challenge(models.Model):
    name = models.CharField(max_length=255)
    purchase_max = models.DecimalField(max_digits=9, decimal_places=2)
    dollar_max = models.DecimalField(max_digits=9, decimal_places=2)
    users = models.ManyToManyField(User, related_name='challenges')
    categories = models.ManyToManyField(Category, related_name='challenges')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
