from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('users/register', views.register_user),
    path('users/login', views.login),
    path('success', views.success_page),
    path('logout', views.logout)
]