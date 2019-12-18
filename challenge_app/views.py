from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Purchase, Category, Challenge
from login_app.models import User

def index(request):
    return redirect(f'/app/users/{request.session["user_id"]}')

def user_page(request, user_id):
    return render(request, 'userprofile.html')

def add_purchase_page(request, user_id):
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user_purchases': Purchase.objects.filter(user = this_user),
        'categories': Category.objects.all()
    }
    return render(request, 'create_purchase.html', context)

def create_purchase(request, user_id):
    fixedcategory=request.POST['category']
    tempdict={
            "category": request.POST['category']
        }
    if request.POST['category']=='newcategory':
        fixedcategory=request.POST['newcategory']
        tempdict['category']=request.POST['newcategory']

    errors = Purchase.objects.basic_validator(request.POST)
    errors.update(Category.objects.basic_validator(tempdict))
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/app/users/{request.session["user_id"]}/purchases/new')

    Purchase.objects.create(item_name=request.POST['item'],
                            location=request.POST['location'],
                            amount=float(request.POST['amount']),
                            category=Category.objects.get(name=fixedcategory),
                            user=User.objects.get(id=request.session['user_id']))
    return redirect(f'/app/users/{request.session["user_id"]}/purchases')


def user_purchases(request, user_id):
    this_user= User.objects.get(id=request.session['user_id'])
    context ={
        
        "user_purchases": Purchase.objects.filter(user=this_user)
    }
    return render(request, 'user_purchases.html', context)

def add_challenge(request, user_id):
    context={
        "categories": Category.objects.all()
    }
    return render(request, 'add_challenge.html', context)

def create_challenge(request, user_id):
    errors = Challenge.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/app/users/{request.session["user_id"]}/add_challenge')
    return HttpResponse('creating a challenge')


