from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import Http404

def check_user_able_to_see_page(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            raise Http404

        return wrapper

    return decorator

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):


            group= None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized')
        return wrapper_func
    return decorator


def admin_only(view_func):
        def wrapper_func(request, *args, **kwargs):
            group= None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            if group == 'users':
                return redirect('user-page')
            if group == 'admin':
                return view_func(request, *args, **kwargs)
        return wrapper_func
 