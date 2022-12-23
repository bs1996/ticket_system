from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import NewUserForm
from .forms import LoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.contrib import messages
from .models import User, Agent
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            surname = request.POST['surname']
            company = request.POST['company']
            phone = request.POST['phone']
            email_address = request.POST['email_address']
            password = make_password(str(request.POST['password']), salt=None, hasher='default')
            form = User(name=name, surname=surname, company=company,
                     phone=phone, email_address=email_address, password=password)
            form.save()
            messages.success(request, 'Your account has been created. You can log in now!')
            return redirect('/login')
    else:
        form = NewUserForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def index(request):
    title = "support"
    return render(request, 'base.html', {'title': title})


def login(request):
    submitted = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sign_in/?submitted=True')
    else:
        form = LoginForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'sign_in.html', {'form': form, 'submitted': submitted})
