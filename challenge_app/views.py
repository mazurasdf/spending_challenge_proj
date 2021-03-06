from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Purchase, Category, Challenge
from login_app.models import User

def index(request):
    return redirect(f'/app/users/{request.session["user_id"]}')

def user_page(request, user_id):
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')
    if user_id != request.session['user_id']:
        return redirect('/')
    return render(request, 'userprofile.html')

def add_purchase_page(request, user_id):
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')
    if user_id != request.session['user_id']:
        return redirect('/')
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user_purchases': Purchase.objects.filter(user = this_user),
        'categories': Category.objects.all()
    }
    return render(request, 'create_purchase.html', context)

def create_purchase(request, user_id):
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')
    if user_id != request.session['user_id']:
        return redirect('/')

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
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')
    if user_id != request.session['user_id']:
        return redirect('/')

    this_user= User.objects.get(id=request.session['user_id'])
    context ={
        "user": this_user,
        "user_purchases": Purchase.objects.filter(user=this_user)
    }
    return render(request, 'user_purchases.html', context)

def add_challenge(request, user_id):
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')
    if user_id != request.session['user_id']:
        return redirect('/')

    context={
        "categories": Category.objects.all()
    }
    return render(request, 'add_challenge.html', context)

def create_challenge(request, user_id):
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')
    if user_id != request.session['user_id']:
        return redirect('/')

    errors = Challenge.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/app/users/{request.session["user_id"]}/add_challenge')
    this_user=User.objects.get(id=request.session['user_id'])

    challenge_created=Challenge.objects.create(name=request.POST['name'], purchase_max=request.POST['purchase_max'], dollar_max=request.POST['dollar_max'])
    challenge_created.users.add(this_user)

    for category in Category.objects.all():
        if category.name in request.POST:
            challenge_created.categories.add(category)
 
    return redirect(f"/app/users/{request.session['user_id']}/challenges/{challenge_created.id}")

def show_challenge(request, user_id, challenge_id):
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')

    this_challenge = Challenge.objects.get(id=challenge_id)
    context ={
        "challenge_to_show":Challenge.objects.get(id=challenge_id),
        "user":User.objects.get(id=request.session['user_id']),
        # "user_purchases": Purchase.objects.filter(category__in=this_challenge.categories.all(),SDVc
        #                                           user=User.objects.get(id=request.session['user_id']))
        'user_list': []
    }

    for user in this_challenge.users.all():
        purchases = Purchase.objects.filter(category__in=this_challenge.categories.all(), user=User.objects.get(id=user.id))
        sum = 0
        for item in purchases:
            sum += item.amount
        context['user_list'].append({
            'user': user,
            'purchases': purchases,
            'purchase_total': sum,
        })
        
    return render(request, 'challengepage.html', context)


def add_challenger(request, challenge_id):
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')

    # challenger_to_add: 
    challenge_to_add_to= Challenge.objects.get(id=challenge_id)
    user_to_add= User.objects.get(email=request.POST['emailinvite'])
    

    challenge_to_add_to.users.add(user_to_add)
    # context={
    #     "added_user": User.objects.get(email=request.POST['emailinvite'])
       
    # }
    return redirect(f"/app/users/{request.session['user_id']}/challenges/{challenge_to_add_to.id}")


def user_challenges(request, user_id):
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')
    if user_id != request.session['user_id']:
        return redirect('/')
        
    this_user=User.objects.get(id=user_id)
    context={
        "challenges": this_user.challenges.all()

    }
    return render(request, 'user_challenges.html', context)
