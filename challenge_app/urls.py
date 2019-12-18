from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('users/<int:user_id>', views.user_page),
    path('users/<int:user_id>/purchases/new', views.add_purchase_page),
    path('users/<int:user_id>/purchases/create', views.create_purchase),
    path('users/<int:user_id>/purchases', views.user_purchases),
    path('users/<int:user_id>/add_challenge', views.add_challenge),
    path('users/<int:user_id>/challenges/create', views.create_challenge),
    path('users/<int:user_id>/challenges/<int:challenge_id>', views.show_challenge),
    path('users/add_challenger_to_challenge/<int:challenge_id>', views.add_challenger)
    ]