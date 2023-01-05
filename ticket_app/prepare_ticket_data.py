from .models import Customer, Ticket,screenshots
import json, datetime


def prepare_data(number, comment):
    ticket = Ticket.objects.filter(number=number)
    user_id = ticket[0].User_id
    user_name = ticket[0].User.first_name
    user_lastname = ticket[0].User.last_name
    user_mail = ticket[0].User.email
    customer = Customer.objects.filter(user_id=user_id)
    company = customer[0].company
    phone = customer[0].phone

    ticket_status = ticket[0].status
    ticket_agent = ticket[0].assigned_to
    ticket_description = ticket[0].description
    ticket_serial_number = ticket[0].serial_number_or_client_name
    comments_old = ticket[0].comments
    if comments_old == "" or 0:
        arr = []
        comments_old_arr = {"comments": arr}
        comments_old = json.dumps(comments_old_arr)
    comments_old_loads = json.loads(comments_old)
    comments_old_comments = comments_old_loads['comments']
    if comment != 0:
        comments_new = chat_data(number, comments_old, comment, user_name, user_lastname)
    else:
        comments_new = comments_old_comments
    images = screenshots.objects.filter(ticket_numb=number)

    ticket_data = [ticket_status, user_name, user_lastname, user_mail, phone, company, ticket_serial_number,
                   ticket_agent]
    text = ['status', 'name', 'surname', 'mail address', 'phone number', 'company', 'serial number or client name',
            'assigned to']
    return ticket_data, comments_new, ticket_description, text, images


def chat_data(number, comments, comment, name, lastname):
    time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S').split('.')
    if comments == "" or 0:
        arr = []
        comments_dict1 = {"comments": arr}
        comments = json.dumps(comments_dict1)
    comments_dict = json.loads(comments)
    comments_arr_old = comments_dict['comments']
    message = str(time) + " " + str(name) + " " +str(lastname) + ": " + str(comment)
    comments_arr_old.insert(0, message)
    comments_arr_new = comments_arr_old
    chat = {"comments": comments_arr_new}
    chat_data = json.dumps(chat)
    Ticket.objects.filter(number=number).update(comments=chat_data)
    return comments_arr_new


def prepare_data_agent(number, request):

    current_user = request.user
    ticket = Ticket.objects.filter(number=number)
    if 'add_comment' in request.POST:
        comment = request.POST['add_comment']
    else:
        comment = 0
    if 'field' in request.POST:
        status = request.POST['field']
    else:
        status = ticket[0].status
    if status != 0 and status != "Change status":
        Ticket.objects.filter(number=number).update(status=status)
    user_id = ticket[0].User_id
    agent_name = current_user.first_name
    agent_surname = current_user.last_name
    user_name = ticket[0].User.first_name
    user_lastname = ticket[0].User.last_name
    user_mail = ticket[0].User.email
    customer = Customer.objects.filter(user_id=user_id)
    company = customer[0].company
    phone = customer[0].phone
    ticket_status = ticket[0].status
    ticket_agent = ticket[0].assigned_to
    ticket_description = ticket[0].description
    ticket_serial_number = ticket[0].serial_number_or_client_name
    ticket_team = ticket[0].team
    comments_old = ticket[0].comments
    if comments_old == "" or 0:
        arr = []
        comments_old_arr = {"comments": arr}
        comments_old = json.dumps(comments_old_arr)
    comments_old_loads = json.loads(comments_old)
    comments_old_comments = comments_old_loads['comments']
    if comment != 0:
        comments_new = chat_data(number, comments_old, comment, agent_name, agent_surname)
    else:
        comments_new = comments_old_comments
    images = screenshots.objects.filter(ticket_numb=number)
    ticket_data = [ticket_status, user_name, user_lastname, user_mail, phone, company, ticket_serial_number,
                   ticket_agent, ticket_team]
    text = ['status', 'name', 'surname', 'mail address', 'phone number', 'company', 'serial number or client name',
            'assigned to', 'team']
    return ticket_data, comments_new, ticket_description, text, images
