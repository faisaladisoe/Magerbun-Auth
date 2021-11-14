from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from menu_api import views

app_name = 'menu_api'

urlpatterns = [
    path('', views.MenuList.as_view(), name = 'Menu List'),
    path('<str:pk>/', views.MenuDetail.as_view(), name = 'Menu Detail')
]
urlpatterns = format_suffix_patterns(urlpatterns)