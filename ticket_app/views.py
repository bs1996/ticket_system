from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.contrib import messages
from .models import User, Agent, Customer, Ticket, screenshots, Order
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, CustomerForm, TicketForm, OrderForm, AddCommentForm, AddCommentForm_Agent,\
    ImageForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from .prepare_ticket_data import prepare_data, prepare_data_agent
from django.core.files.storage import FileSystemStorage


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
        current_user = request.user.id
        agent = Agent.objects.filter(user_id=current_user)
        if agent.exists():
            response = redirect('/')
            response.set_cookie('Agent', '1')
        else:
            response = redirect('/')
        return response

    else:
        form = LoginForm()
        return render(request, 'sign_in.html', {'form': form})


def signout(request):
    logout(request)
    response = redirect('/')
    response.set_cookie('Agent', '1', max_age=0)
    return response


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
            assigned_to = ''
            status = 'In Progress'
            team = 'L1'
            SLA = '0'
            comments = ''
            ticket = Ticket(User=ticket_owner, number=number, description=description,
                            serial_number_or_client_name=serial_number_or_client_name, type=type, SLA=SLA,
                            assigned_to=assigned_to, team=team, status=status, comments=comments)
            ticket.save()
            ticket = Ticket.objects.latest('id')
            ticket.number = ticket.id + 1000
            ticket.save()
            return redirect('/')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})


def order(request):

    return render(request, 'order.html')


def my_tickets(request):
    title = "tickets"
    user = request.user
    id = user.id
    tickets = Ticket.objects.filter(User_id=id)

    num = []
    for ticket in tickets:
        num.append(ticket.number)

    return render(request, 'my_tickets.html', {'title': title, 'num': num})


def incident_user(request, number):
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        form2 = ImageForm(request.POST, request.FILES)
        if form2.is_valid():
            image = request.FILES['image'] if 'image' in request.FILES else False
            if image:
                form2.save()
                screen_numb = screenshots.objects.latest('id')
                screen_numb.ticket_numb = number
                screen_numb.save()
            form2 = ImageForm()
            form = AddCommentForm()
            ticket_data, comments, ticket_description, text, images = prepare_data(number, request)

            return render(request, 'Incident_user.html', {'number': number, 'ticket_data': ticket_data, 'text': text,
                                                           'chat': comments, 'description': ticket_description,
                                                           'form': form, 'form2': form2, 'images': images})
        if form.is_valid():
            comment = request.POST['add_comment']
            form = AddCommentForm()
            form2 = ImageForm()

            ticket_data, comments, ticket_description, text, images = prepare_data(number, request)
            return render(request, 'Incident_user.html', {'number': number, 'ticket_data': ticket_data, 'text': text,
                                                   'chat': comments, 'description': ticket_description,
                                                   'form': form, 'form2': form2, 'images': images})
    else:
        form = AddCommentForm()
        form2 = ImageForm()

        ticket_data, comments, ticket_description, text, images = prepare_data(number, request)
        return render(request, 'Incident_user.html', {'number': number, 'ticket_data': ticket_data, 'text': text,
                                                      'chat': comments, 'description': ticket_description,
                                                      'form': form, 'form2': form2, 'images': images})


def all_tickets(request):
    title = "tickets"

    tickets = Ticket.objects.all()

    num = []

    for ticket in tickets:
        num.append(ticket)

    return render(request, 'All_tickets.html', {'title': title, 'num': num})


def incident_agent(request, number):
    if request.method == 'POST':
        form = AddCommentForm_Agent(request.POST)
        form2 = ImageForm(request.POST, request.FILES)
        if form2.is_valid():
            image = request.FILES['image'] if 'image' in request.FILES else False
            if image:
                form2.save()
                screen_numb = screenshots.objects.latest('id')
                screen_numb.ticket_numb = number
                screen_numb.save()
            form2 = ImageForm()
            form = AddCommentForm_Agent()
            ticket_data, comments, ticket_description, text, images = prepare_data_agent(number, request)

            return render(request, 'incident_agent.html', {'number': number, 'ticket_data': ticket_data, 'text': text,
                                                           'chat': comments, 'description': ticket_description,
                                                           'form': form, 'form2': form2, 'images': images})
        if form.is_valid():
            form = AddCommentForm_Agent()
            ticket_data, comments, ticket_description, text, images = prepare_data_agent(number, request)
            return render(request, 'incident_agent.html', {'number': number, 'ticket_data': ticket_data, 'text': text,
                                                   'chat': comments, 'description': ticket_description,
                                                   'form': form, 'form2': form2, 'images': images})
    else:
        form = AddCommentForm_Agent()
        form2 = ImageForm()

        ticket_data, comments, ticket_description, text, images = prepare_data_agent(number, request)
        return render(request, 'incident_agent.html', {'number': number, 'ticket_data': ticket_data, 'text': text,
                                                      'chat': comments, 'description': ticket_description,
                                                      'form': form, 'form2': form2, 'images': images})


def admin_rights(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            current_user = request.user
            description = request.POST['description']
            print(description)
            order = Order(User=current_user, number=0, description=description, status='In progress',
                          category='admin rights')
            order.save()
            order = Order.objects.latest('id')
            order.number = order.id + 1000
            order.save()
            return redirect('/')
    else:
        form = OrderForm()
        return render(request, 'admin_rights.html', {'form': form})


def new_smartcard(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            current_user = request.user
            description = request.POST['description']
            print(description)
            order = Order(User=current_user, number=0, description=description, status='In progress',
                          category='smartcard')
            order.save()
            order = Order.objects.latest('id')
            order.number = order.id + 1000
            order.save()
            return redirect('/')
    else:
        form = OrderForm()
        return render(request, 'order_smartcard.html', {'form': form})


def fileshare_access(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            current_user = request.user
            description = request.POST['description']
            print(description)
            order = Order(User=current_user, number=0, description=description, status='In progress',
                          category='fileshare')
            order.save()
            order = Order.objects.latest('id')
            order.number = order.id + 1000
            order.save()
            return redirect('/')
    else:
        form = OrderForm()
        return render(request, 'fileshare_access.html', {'form': form})


def my_orders(request):
    user = request.user
    id = user.id
    orders = Order.objects.filter(User_id=id)

    num = []
    for order in orders:
        num.append(order.number)

    return render(request, 'my_orders.html', {'num': num})


def order_user(request, number):
    order_results = Order.objects.filter(number=number)
    order = order_results[0]
    return render(request, 'order_user.html', {'number': number,'order': order})