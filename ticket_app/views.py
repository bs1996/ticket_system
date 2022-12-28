from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.contrib import messages
from .models import User, Agent, Customer, Ticket
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, CustomerForm, TicketForm, OrderForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login, logout


def register(request):
    if request.method == 'POST':
        user_form = RegisterUserForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer = Customer.objects.latest('id')
            customer.phone = str(request.POST['phone'])
            customer.company = str(request.POST['company'])
            customer.save()
            return redirect('/login')
    else:
        user_form = RegisterUserForm()
        customer_form = CustomerForm()
    return render(request, 'register.html', {'form': user_form, 'customer_form': customer_form})


def index(request):
    title = "support"
    return render(request, 'base.html', {'title': title})


def sign_in(request):
    if request.method == "POST":
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is None:
            return HttpResponse("Invalid credentials.")
        login(request, user)
        return redirect('/')

    else:
        form = LoginForm()
        return render(request, 'sign_in.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('/')


def contact(request):
    title = 'contact'
    return render(request, 'contact.html', {'title': title})


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            current_user = request.user
            number = 0
            description = request.POST['description']
            serial_number_or_client_name = request.POST['serial_number_or_client_name']
            type = request.POST['type']
            ticket_owner = current_user
            assigned_to = 'Bartosz Stefaniak'
            status = 'In Progress'
            team = 'L1'
            SLA = '0'
            ticket = Ticket(User=ticket_owner, number=number, description=description,
                            serial_number_or_client_name=serial_number_or_client_name, type=type, SLA=SLA,
                            assigned_to=assigned_to, team=team, status=status)
            ticket.save()
            ticket = Ticket.objects.latest('id')
            ticket.number = ticket.id + 1000
            ticket.save()
            return redirect('/')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})


def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = OrderForm()
    return render(request, 'order.html', {'form': form})


def my_tickets(request):
    title = "tickets"
    user = request.user
    id = user.id
    tickets = Ticket.objects.filter(User_id=id)

    num = []
    for ticket in tickets:
        num.append(ticket.number)
    print(num)
    return render(request, 'my_tickets.html', {'title': title, 'num': num})
