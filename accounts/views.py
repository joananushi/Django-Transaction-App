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
from django.contrib.auth.models import *
from django.contrib.auth.models import Group
from django.db import IntegrityError
from .decorators import unauthenticated_user, allowed_users, admin_only, check_user_able_to_see_page
from datetime import datetime, timedelta



@login_required(login_url='login_view')
def dashboard(request):
    users = User.objects.all()
    transaction= Transaction.objects.all()
    status_choices = Transaction._meta.get_field('status').choices
    
    context={'users': users,
             'transaction':transaction,
             'status_choices':status_choices
             }

    return render(request, 'accounts/dashboard.html', context )

def usertransactions(request, pk):
    user = User.objects.get(id=pk)
    user_transactions = Transaction.objects.all()
    
    # # Loop through each transaction and set the payer attribute to the logged-in user
    # for transaction in user_transactions:
    #     transaction.payer = request.user
    
    context = {
        'user': user,
        'user_transactions': user_transactions,
    }

    return render(request, 'accounts/user_transactions.html', context)


def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.payee = form.cleaned_data['payee']
            transaction.save()
            return redirect('usertransactions')
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

        context = {'form': form}
        return render(request, 'accounts/edit_transaction.html', context, date_limit)
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
    if request.method == 'POST':

        logged_user = User.objects.get(id=pk)
        logged_user.first_name = request.POST.get('first_name')
        logged_user.last_name = request.POST.get('last_name')
        if 'profilepic' in request.FILES:
            logged_user.profile_image = request.FILES['profilepic']
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
    if request.user.is_authenticated:
        return redirect('dashboard') 
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                try:
                    user_form =form.save()
                    email= form.cleaned_data.get('email')
                    group = Group.objects.get(name='user')
                    User.profilepic = 'profilepic.jpg'
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
    if request.user.is_authenticated:
        return redirect('dashboard') 
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me') 
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not remember_me:
                    request.session.set_expiry(0)
                login(request, user)
                return redirect('dashboard')  
            #     if user.groups.filter(name='admin').exists():
            #         return redirect('dashboard')  # Redirect admin to the dashboard
            #     else:
            #         return redirect('usertransactions')  # Redirect non-admin to the transaction page
            else:
                messages.info(request, 'Username or password is incorrect.')

    return render(request, 'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect('login_view')