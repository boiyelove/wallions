import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserProfile
from .utils import email_password, code_generator



class LoginForm(forms.Form):
	username = forms.CharField(min_length=6)
	password = forms.CharField()


	def clean_username(self):
		username = self.cleaned_data.get('username')
		username = username.strip()
		try:
			this_user = User.objects.get(username = username)
		except User.DoesNotExist:
			raise forms.ValidationError('User with this username does not exist')
		if not this_user.is_active:
			raise forms.ValidationError('Sorry you are not allowed to log in, contact support team')
		return username

	def clean_password(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		try:
			this_user = User.objects.get(username = username)
		except User.DoesNotExist:
			raise forms.ValidationError('User with this username does not exist')
		if not this_user.is_active:
			raise forms.ValidationError('Sorry you are not allowed to log in, contact support team')
		if not this_user.check_password(password):
			raise forms.ValidationError('Please check that your details you provided are correct')
		return password


	def login_user(self, request):
		cleaned = super(LoginForm, self).clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError("An error occcured, please check your password or call admin")
		return login(request, user)

class RegisterForm(forms.Form):
	username = forms.CharField(min_length = 6)
	email = forms.EmailField()
	email_again = forms.EmailField()
	password = forms.CharField(min_length=8)
	password_again = forms.CharField(min_length=8)
	full_name = forms.CharField(max_length =100, min_length = 3, required = False)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		username = username.strip().lower()
		if re.search(r'\W+', username):
			raise forms.ValidationError('Only alphabets and numbers allowed')
		if len(username) < 6:
			raise forms.ValidationError('Username has to be a minimum of 6 chracters long')
		try:
			this_user = User.objects.get(username = username)
			raise forms.ValidationError('Username already exist')
		except User.DoesNotExist:
			return username

	def clean_email_again(self):
		email = self.cleaned_data.get('email').lower()
		email1 = self.cleaned_data.get('email_again').lower()
		if email != email1:
			raise forms.ValidationError('Email addresses do not match')
		try:
			User.objects.get(email = email)
			raise forms.ValidationError('Email address already exists')
		except User.DoesNotExist:
			return email.lower()


	def clean_password_again(self):
		password = self.cleaned_data.get('password').strip()
		password_again = self.cleaned_data.get('password_again').strip()
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		full_name = self.cleaned_data.get('full_name')
		if len(password) < 6:
			raise forms.ValidationError('Username has to be a minimum of 6 chracters long')
		if password != password_again:
			raise forms.ValidationError('Passwords do not match')
		if password == username:
			raise forms.ValidationError('Password and Username cannot be the same')
		elif password == email:
			raise forms.ValidationError('You may not set your email address as your password')
		elif password == full_name:
			raise forms.ValidationError('You may not set your name as you passord')
		return password

	def register_user(self):
		user = User.objects.create(username = self.cleaned_data.get('username'),
			 password = self.cleaned_data.get('password'), 
			 email=self.cleaned_data.get('email'))
		obj, created = UserProfile.objects.get_or_create(user = user)
		full_name = self.cleaned_data.get('full_name')
		if full_name:
			obj.full_name = full_name
		else:
			obj.full_name = self.cleaned_data.get('username')
		obj.save()




class UserProfileForm(forms.ModelForm):
	full_name = forms.CharField(max_length = 50, required=True)
	headshot = forms.ImageField(required=False)

	class Meta:
		model = UserProfile
		fields = ('full_name', 'headshot')


class PasswordRequestForm(forms.Form):
	email = forms.EmailField()
	email_again = forms.EmailField()


	def clean(self):
		email = self.cleaned_data.get('email')
		email_again = self.cleaned_data.get('email_again')
		if email != email_again:
			raise forms.ValidationError('The email addresses you entered are not correct')
		try:
			u = User.objects.get(email = email)
		except:
			raise forms.ValidationError("Something is not right. We couldn't find an account with that email")
		return super(PasswordRequestForm, self).clean()

	def done(self):
		email = self.cleaned_data.get('email')
		u = User.objects.get(email = email)
		password = code_generator(u.email)
		password = password[:10]
		u.set_password(password)
		u.save()
		email_password(u, password)




class PasswordChangeForm(forms.Form):
	password = forms.CharField()
	password_again = forms.CharField()

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request')
		super(PasswordChangeForm, self).__init__(*args, **kwargs)



	def clean_password_again(self):
		password = self.cleaned_data.get('password')
		password_again = self.cleaned_data.get('password_again')
		u = self.request.user
		if not u.is_authenticated:
			raise forms.ValidationError("Something is not right. We couldn't find an account with that email")
		if len(password) < 6:
			raise forms.ValidationError('Username has to be a minimum of 6 chracters long')
		if password != password_again:
			raise forms.ValidationError('Passwords do not match')
		if password == u.username:
			raise forms.ValidationError('Password and Username cannot be the same')
		elif password == u.email:
			raise forms.ValidationError('You may not set your email address as your password')
		elif password == u.userprofile.full_name:
			raise forms.ValidationError('You may not set your name as you passord')
		return password

	def done(self):
		password = self.cleaned_data.get(password)
		u = self.request.user
		u.set_password = password
		u.save()
		email_password(u, password)


		






