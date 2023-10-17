from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'admin', 'created_at', 'updated_at')

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
admin.site.register(Transaction)
# admin.site.register(payer_payee)