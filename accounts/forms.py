from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    first_name=forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    last_name=forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model= User
        fields=['username','first_name','last_name','email', 'password1','password2']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'category', 'payment_method', 'reference_number','attachments']



        
# class LoginForm(AuthenticationForm):
#     first_name = forms.CharField(widget=TextInput())
#     last_name = forms.CharField(widget=TextInput())
#     email = forms.CharField(widget=TextInput())
#     password = forms.CharField(widget=PasswordInput())