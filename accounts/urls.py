from django.urls import path     
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usertransactions/<int:pk>/', views.usertransactions, name='usertransactions'),
    path('', views.index, name='index'),	
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout', views.logout_view, name='logout_view'),
    path('profile/<int:pk>/', views.user_profile, name='user_profile'),
    path('profile/<int:pk>/edit/', views.edit_user_data, name='edit_user_data'),
    path('profile/<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('make-transaction/', views.make_transaction, name='make_transaction'),
    path('edit-transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
]


