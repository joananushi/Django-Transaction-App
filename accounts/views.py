from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import TransactionForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import *
from .forms import CreateUserForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.contrib.auth.models import Group
from django.db import IntegrityError
from .decorators import unauthenticated_user
from datetime import datetime, timedelta
from django.http import Http404, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .utils import delete_image


User=get_user_model()


@csrf_exempt
def update_transaction_status(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        new_status = request.POST.get('new_status')
        try:
            transaction = Transaction.objects.get(pk=transaction_id)
            transaction.status = new_status
            transaction.save()
            return JsonResponse({'success': True})
        except Transaction.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Transaction not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def dashboard(request):
    users = User.objects.all()
    transaction= Transaction.objects.all()
    status_choices = Transaction._meta.get_field('status').choices
    admin = 1 if request.user.is_staff else 0 

    
    context={'users': users,
             'transaction':transaction,
             'status_choices':status_choices,
             'admin': admin,
             'user': request.user
             
             }

    return render(request, 'accounts/dashboard.html', context )
@login_required
def usertransactions(request, pk):
    user = User.objects.get(id=pk)
    user_transactions = Transaction.objects.filter(user=pk)
    is_admin = 0
   

    context = {
        'user': user,
        'user_transactions': user_transactions,
         'is_admin':is_admin
         
    }

    return render(request, 'accounts/user_transactions.html', context)

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.payee = form.cleaned_data['payee']
            transaction.save()
            return redirect('usertransactions', pk=request.user.pk)
        else:
            form_errors = form.errors
            print(form_errors)
    else:
        form = TransactionForm(request.user)

    context = {'form': form}
    return render(request, 'accounts/make_transaction.html', context)


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

        context = {'form': form,
                   'date_limit': date_limit}
        return render(request, 'accounts/edit_transaction.html', context)
    else:
        return redirect('list_transactions')

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    date_limit = datetime.now() - timedelta(days=5)
    if transaction.date > date_limit:
        transaction.delete()
        
    return redirect('list_transactions', date_limit)


@login_required
def user_profile(request, pk):
   
    logged_user = User.objects.get(id=pk)
    context = {'user': logged_user}
    return render(request, 'accounts/user_profile.html', context)

@login_required
def edit_user_data(request, pk):
    logged_user = User.objects.get(id=pk)
    if request.method == 'POST':
        logged_user.first_name = request.POST.get('first_name')
        logged_user.last_name = request.POST.get('last_name')
        if 'profilepic' in request.FILES:
            # Delete the old profile image
            if logged_user.profile_image:
                delete_image(logged_user.profilepic.path)
            logged_user.profile_image = request.FILES['profilepic']
        logged_user.save()
        return redirect('user_profile', pk=pk)
    else:
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
    if request.user.is_authenticated:
        return redirect('dashboard') 
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save(commit=False) 
                    user.admin = 0
                    user.is_active=True
                    password = form.cleaned_data.get("password")
                    user.set_password(password)
                    user.save()
                    
                    user.profilepic = 'profilepic.jpg'
                    if user.password == request.POST['password2']:
                        new_user = authenticate(username=user.username, password=password)
                        login(request, new_user, backend='accounts.backends.AccountNoBackend')
                        messages.success(request, 'Account created!')
                        return redirect('login_view')
                    else:
                        messages.error(request, 'Passsword do not match!')
                        return redirect('register')
                except IntegrityError:
                    messages.error(request, 'Username already exists. Please choose a different username.')
        context = {'form': form}
    return render(request, 'accounts/register.html', context)
    
def index(request):
    return redirect('login_view')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.admin == 1:
            return redirect('dashboard')
        else:
           return redirect('usertransactions', pk=request.user.pk)
    else:
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            user = authenticate(username=username, password=password)
            login(request, user, backend='accounts.backends.AccountNoBackend')
            messages.success(request, 'Welcome, {}!' .format(user.first_name))
            if user.admin == 1:
                     return redirect('dashboard')  # Redirect admin to the dashboard
            else:
                     return redirect('usertransactions', pk=request.user.pk)

    context = {"form": form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login_view')