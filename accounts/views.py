from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms  import UserCreationForm
from .forms import TransactionForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db import IntegrityError
from .decorators import unauthenticated_user, allowed_users, admin_only, check_user_able_to_see_page
from datetime import datetime, timedelta


@login_required(login_url='login_view')

def dashboard(request):
    users = User.objects.all()
    context={'users': users}

    return render(request, 'accounts/dashboard.html', context )

def usertransactions(request, pk):
    logged_user = User.objects.get(id=pk)
    transactions = Transaction.objects.filter(user=logged_user)

    context = {
        'user': logged_user,
        'transactions': transactions,
    }

    return render(request, 'user_transactions.html', context)

def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('usertransactions', pk=request.user.id)
    else:
        form = TransactionForm()

    context = {'form': form}
    return render(request, 'make_transaction.html', context)


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    date_limit = datetime.now() - timedelta(days=5)
    if transaction.date > date_limit:
        if request.method == 'POST':
            form = TransactionForm(request.POST, instance=transaction)
            if form.is_valid():
                form.save()
                return redirect('usertransactions')
        else:
            form = TransactionForm(instance=transaction)

        context = {'form': form}
        return render(request, 'edit_transaction.html', context)
    else:
        return redirect('list_transactions')

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    date_limit = datetime.now() - timedelta(days=5)
    if transaction.date > date_limit:
        transaction.delete()
        
    return redirect('list_transactions')



@login_required
def user_profile(request, pk):
   
    logged_user = User.objects.get(id=pk)
    context = {'user': logged_user}
    return render(request, 'accounts/user_profile.html', context)

@login_required
def edit_user_data(request, pk):
    if request.method == 'POST':
       
        logged_user = User.objects.get(id=pk)
        logged_user.first_name = request.POST.get('first_name')
        logged_user.last_name = request.POST.get('last_name')
        logged_user.save()
        return redirect('user_profile', pk=pk)

    else:
        logged_user = User.objects.get(id=pk)
        context = {'user': logged_user}
        return render(request, 'accounts/edit_user_data.html', context)
@login_required
def delete_user(request, pk):
    user_to_delete = User.objects.get(id=pk)
    if request.method == 'POST':
        user_to_delete.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('dashboard')

    context = {'user_to_delete': user_to_delete}
    return render(request, 'accounts/delete_user.html', context)

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                user_form =form.save()
                email= form.cleaned_data.get('email')
                group = Group.objects.get(name='users')
                user_form.groups.add(group)
                messages.success(request, 'Account created!')
                return redirect('login_view')
            except IntegrityError:
                messages.error(request, 'Username already exists. Please choose a different username.')



    context = {'form': form}
    return render(request, 'accounts/register.html', context)
    
def index(request):
    return redirect('login_view')
 
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard') 
            #return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.info(request, 'Email or password is incorrect.')
    context={}
    return render(request, 'accounts/login.html', context)



def logout_view(request):
    logout(request)
    return redirect('login_view')