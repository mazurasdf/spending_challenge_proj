from django.db import models
from datetime import date, datetime
import re

class User_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
            errors['name'] = 'Names must be at least 2 characters'

        try:
            User.objects.get(email=post_data['email'])
            errors['email'] = 'Email already in use'
        except:
            pass
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid email'

        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if post_data['password'] != post_data['confirm_password']:
            errors['password'] = 'Passwords must match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=320)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()