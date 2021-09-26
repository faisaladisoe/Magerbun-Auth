from django.contrib import admin

from account.models import Account
from account.forms import AccountAdmin

# Register your models here.
admin.site.register(Account, AccountAdmin)