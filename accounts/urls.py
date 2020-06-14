from django.contrib import admin
from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    #path('', views.index, name='home'),
    path('accounts/sign_up/', views.sign_up, name='sign_up'),
]