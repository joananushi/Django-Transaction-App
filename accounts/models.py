from django.db import models
from django.contrib.auth.models import User
import re
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.templatetags.static import static

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def default_profile_pic():
    return static("accounts/images/profile_pic.jpg")

class User(models.Model):
    username = models.CharField(max_length=225, null=True, unique=True)
    first_name= models.CharField(max_length=225, null=True)
    last_name= models.CharField(max_length=225, null=True)
    email = models.CharField(max_length=225, null=True, unique=True)
    password=models.CharField(max_length=225, null=True)
    admin=models.IntegerField(default=0)
    profilepic= models.ImageField(upload_to='images/', default=default_profile_pic)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return self.username

class Transaction(models.Model):
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    date= models.DateField(auto_now_add=True)
    description=models.TextField()
    category=models.CharField(
        max_length=20,
        choices=[
            ('income', 'Income'),
            ('expenses', 'Expenses'),
            ('investments', 'Investments'),
            ('transfers', 'Transfers'),
        ]
    )    
    status= models.CharField(
        max_length=20, default='Pending',
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed'),
        ]
    )
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payee= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transaction_receiver')
    payment_method = models.CharField(max_length=50)
    reference_number=models.CharField(max_length=50)
    attachments = models.FileField(upload_to='transaction_attachments/')
    #attachments = models.FileField(upload_to='media/transaction_attachments/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
