from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('users/<int:user_id>', views.user_page),
    path('users/<int:user_id>/purchases/new', views.add_purchase_page),
    path('users/<int:user_id>/purchases/create', views.create_purchase),
    path('users/<int:user_id>/purchases', views.user_purchases)
]