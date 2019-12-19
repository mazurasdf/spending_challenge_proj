from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import User


def index(request):
    if "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect(f'/app/users/{request.session["user_id"]}')
    return render(request, 'index.html')

def register_user(request):
    if request.method != 'POST':
        return redirect('/')

    errors = User.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    hash_pass = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=request.POST['first_name'],
                                   last_name=request.POST['last_name'],
                                   email=request.POST['email'],
                                   password=hash_pass)

    messages.info(request, 'Account created successfully')
    return redirect('/')


def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, 'Invalid email or password')
        return redirect('/')

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['user_name'] = user.first_name + ' ' + user.last_name
        return redirect('/success')
    else:
        messages.error(request, 'Invalid email or password')
        return redirect('/')


def success_page(request):
    if 'user_id' in request.session:
        return redirect('/app')
    else:
        messages.error(request, 'Please enter login credentials')
        return redirect('/')


def logout(request):
    del request.session['user_id']
    del request.session['user_name']
    return redirect('/')
