from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Purchase, Category, Challenge
from login_app.models import User

def index(request):
    return redirect(f'/app/users/{request.session["user_id"]}')

def user_page(request, user_id):
    return render(request, 'user_page.html')

def add_purchase_page(request, user_id):
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user_purchases': Purchase.objects.filter(user = this_user)
    }
    return render(request, 'create_purchase.html', context)

def create_purchase(request, user_id):
    errors = Purchase.objects.basic_validator(request.POST)
    errors.update(Category.objects.basic_validator(request.POST))
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/app/users/{request.session["user_id"]}/purchases/new')

    Purchase.objects.create(item_name=request.POST['item'],
                            location=request.POST['location'],
                            amount=float(request.POST['amount']),
                            category=Category.objects.get(name=request.POST['category']),
                            user=User.objects.get(id=request.session['user_id']))
    return redirect(f'/app/users/{request.session["user_id"]}/purchases/new')
