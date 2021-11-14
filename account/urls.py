from account import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'

urlpatterns = [
    path('test/', views.accountTest, name = 'Account Test'),
    path('register/', views.accountRegister, name = 'Account Register'),
    path('login/', obtain_auth_token, name = 'Account Login'),
    path('<str:role>/<str:email>/', views.accountProfile, name = 'Account Profile'),
]