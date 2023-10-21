from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction, User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

class CreateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    first_name=forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    last_name=forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    password=forms.PasswordInput()
    
    class Meta:
        model= User
        fields=['username','first_name','last_name','email', 'password']

class TransactionForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['payee'].queryset = User.objects.exclude(id=user.id)

    
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'category','payee', 'payment_method', 'reference_number','attachments']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'payee': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'attachments': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        

class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.add_error('username', "Account Does Not Exist.")
            elif not user.check_password(password):
                self.add_error('password', "Password Does not Match.")
            elif not user.is_active:
                self.add_error(None, "Account is not Active.")

        return cleaned_data


        
# class LoginForm(AuthenticationForm):
#     first_name = forms.CharField(widget=TextInput())
#     last_name = forms.CharField(widget=TextInput())
#     email = forms.CharField(widget=TextInput())
#     password = forms.CharField(widget=PasswordInput())