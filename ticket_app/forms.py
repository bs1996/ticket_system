from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Agent, Customer, Ticket, Order
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.password_validation import validate_password

# Create your forms here.
CHOICES = (
    ('incident','INCIDENT'),
    ('major', 'MAJOR'),
)

class LoginForm(forms.ModelForm):
	username = forms.CharField(required=True)
	password = forms.CharField(widget=PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def clean(self):
		cleaned_data = super(UserCreationForm, self).clean()
		password = cleaned_data.get("password1")
		password2 = cleaned_data.get("password2")

		if password != password2:
			self.add_error('password2', "Password does not match")
		if validate_password(password):
			self.add_error('password1', "error")

		return cleaned_data


class CustomerForm(forms.ModelForm):

	class Meta:
		model = Customer
		fields = ['company', 'phone']


class TicketForm(forms.ModelForm):
	description = forms.CharField(required=True)
	serial_number_or_client_name = forms.CharField(required=True)
	type = forms.ChoiceField(choices=CHOICES)

	class Meta:
		model = Ticket
		fields = ['description', 'serial_number_or_client_name', 'type']


class OrderForm(forms.ModelForm):
	description = forms.CharField(required=True)


	class Meta:
		model = Order
		fields = ['description']
