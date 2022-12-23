from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Agent
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.password_validation import validate_password

# Create your forms here.


class LoginForm(forms.Form):
	email_address = forms.EmailField(required=True)
	password = forms.CharField(widget=PasswordInput())


class NewUserForm(ModelForm):
	name = forms.CharField(required=True)
	surname = forms.CharField(required=True)
	company = forms.CharField(required=True)
	phone = forms.CharField(required=True)
	email_address = forms.EmailField(required=True)
	password = forms.CharField(widget=PasswordInput())
	password2 = forms.CharField(widget=PasswordInput())

	class Meta:
		model = User
		fields = ('name', 'surname', 'company', 'phone', 'email_address', 'password', 'password2')

	def clean(self):
		cleaned_data = super(NewUserForm, self).clean()
		password = cleaned_data.get("password")
		password2 = cleaned_data.get("password2")

		if password != password2:
			self.add_error('password2', "Password does not match")
		if validate_password(password):
			self.add_error('password', "error")

		return cleaned_data

		#password = make_password(str(password), salt=None, hasher='default')
