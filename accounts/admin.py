from django.contrib import admin

from .models import *


admin.site.register(User)
admin.site.register(Transaction)
# admin.site.register(payer_payee)