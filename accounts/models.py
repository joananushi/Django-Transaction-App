from django.db import models
from django.contrib.auth.models import User
import re
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


  

class User(models.Model):
    username = models.CharField(max_length=225, null=True)
    email = models.CharField(max_length=225, null=True)
    password=models.CharField(max_length=225, null=True)
    admin=models.IntegerField(default=0)
    profilepic=models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    reference_number=models.CharField(max_length=50)
    attachments = models.FileField(upload_to='transaction_attachments/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class payer_payee(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    trasaction=models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)