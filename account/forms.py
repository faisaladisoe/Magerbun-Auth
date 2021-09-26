from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models import Account

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'passwordConfirmation', 'role', 'is_active', 'is_admin', 'is_staff', 'is_superuser']

class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm
    list_display = ('email', 'username', 'role', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('role', 'date_joined', 'email', 'username')

    fieldsets = ()
    list_filter = ()
    filter_horizontal = ()