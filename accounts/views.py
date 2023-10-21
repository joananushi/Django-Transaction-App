from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import TransactionForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import CreateUserForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import *
from django.contrib.auth.models import Group
from django.db import IntegrityError
from .decorators import unauthenticated_user
from datetime import datetime, timedelta
from django.http import Http404, HttpResponse



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

def usertransactions(request, pk):
    user = User.objects.get(id=pk)
    user_transactions = Transaction.objects.all()
    is_admin = 0
   

    context = {
        'user': user,
        'user_transactions': user_transactions,
         'is_admin':is_admin
         
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

# def make_transaction(request):
#     if request.method == 'POST':
#         form = TransactionForm(request.user, request.POST)
#         if form.is_valid():
#             transaction = form.save(commit=False)
#             transaction.user = request.user

#             # Retrieve the payee User instance based on the username or other identifier.
#             payee_username = form.cleaned_data['payee']
#             try:
#                 payee_user = User.objects.get(username=payee_username)
#                 if payee_user:  # Check if the user exists
#                     transaction.payee = payee_user
#                     transaction.save()
#                     return redirect('usertransactions')
#                 else:
#                     raise Http404("Payee not found")
#             except User.DoesNotExist:
#                 raise Http404("Payee not found")  # Handle the case where the payee user doesn't exist.
#         else:
#             form_errors = form.errors
#             print(form_errors)
#     else:
#         form = TransactionForm(request.user)

#     context = {'form': form}
#     return render(request, 'accounts/make_transaction.html', context)

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
                    user = form.save(commit=False) 
                    user.admin = 0
                    user.save()
                    email= form.cleaned_data.get('email')
                    user.profilepic = 'profilepic.jpg'
                    if user.password == request.POST['password2']:
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
 

# def login_view(request):
#     if request.user.is_authenticated:
#         if request.user.admin == 1:
#             return redirect('dashboard')  # Redirect admin to the dashboard
#         else:
#             return redirect('usertransactions', pk=request.user.pk)  # Redirect non-admin to the transaction page
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             remember_me = request.POST.get('remember_me')
#             print(f"Username: {username}, Password: {password}")
#             user = authenticate(request, username=username, password=password)
            
#             if user is not None:

#                 login(request, user , backend='accounts.backends.ModelBackend')
#                 print(f"Authenticated user: {user.username}")
                
#                 if not remember_me:
#                     request.session.set_expiry(0)
#                 if user.admin == 1:
#                     return redirect('dashboard')  # Redirect admin to the dashboard
#                 else:
#                     return redirect('usertransactions', pk=request.user.pk)  # Redirect non-admin to the transaction page
#             else:
#                 messages.error(request, 'Username or password is incorrect.')

#     return render(request, 'accounts/login.html')
# _____________________________________________________________________________


def login_view(request):
    if request.user.is_authenticated:
        if request.is_staff:
            return redirect('dashboard')  # Redirect admin to the dashboard
        else:
            return redirect('usertransactions', pk=request.user.pk)  # Redirect non-admin to the transaction page
    else:
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                remember_me = request.POST.get('remember_me')

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    messages.success(request, 'Welcome!')
                    if user.is_staff:
                        return redirect('dashboard')  # Redirect admin to the dashboard
                    else:
                        return redirect('usertransactions', pk=user.pk)  # Redirect non-admin to the transaction page
                else:
                    messages.error(request, 'Username or password is incorrect.')
        else:
            form = UserLoginForm()

        context = {"form": form}
        return render(request, 'accounts/login.html', context)









        # form = UserLoginForm(request.POST or None)

        # if form.is_valid():
        #     account_no = form.cleaned_data.get("account_no")
        #     password = form.cleaned_data.get("password")
        #     # authenticate with Account No & Password
        #     user = authenticate(account_no=account_no, password=password)
        #     login(request, user, backend='accounts.backends.AccountNoBackend')
        #     messages.success(request, 'Welcome, {}!' .format(user.full_name))
        #     return redirect("home")

        # context = {"form": form,
        #            "title": "Load Account Details",
        #            }

        # return render(request, "accounts/form.html", context)


def logout_view(request):
    logout(request)
    return redirect('login_view')