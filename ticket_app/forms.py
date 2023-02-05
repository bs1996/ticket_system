from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Agent, Customer, Ticket, Order, screenshots
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.password_validation import validate_password

# Create your forms here.
CHOICES = (
    ('incident', 'INCIDENT'),
    ('major', 'MAJOR'),
)
options = (('Change status', 'Change status'), ('Resolved', 'Resolved'),
		   ('In Progress', 'In Progress'), ('Pending', 'Pending'))


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


class OrderForm(forms.Form):
	description = forms.CharField(required=True)


class AddCommentForm(forms.Form):
	add_comment = forms.CharField(required=True)

	def clean(self):
		cleaned_data = super(AddCommentForm, self).clean()
		add_comment = cleaned_data.get("add_comment")

		return cleaned_data


class AddCommentForm_Agent(forms.Form):
	add_comment = forms.CharField(required=True)
	field = forms.ChoiceField(choices=options)
	team = forms.CharField(required=False)
	agent = forms.CharField(required=False)


	def clean(self):
		cleaned_data = super(AddCommentForm_Agent, self).clean()
		add_comment = cleaned_data.get("add_comment")

		return cleaned_data


class ImageForm(forms.ModelForm):
	image = forms.ImageField(required=False)

	class Meta:
		model = screenshots
		fields = ('image',)
