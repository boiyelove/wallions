from django.test import TestCase
from .forms import LoginForm, RegisterForm
# Create your tests here.
#register detail
full_name = "Jerry Laweson"
email = "me@example.com"
password = "13khjfvbvg"
username = 'JerryLawesone'


class FormData(object):

	def __init__(self):
		self.username = username
		self.password = password
		self.full_name = full_name
		self.email = email

	def correct_data(self):
		return (self.username, self.password, self.email, self.full_name)

	def correct_data_username(self):
		return self.username

	def correct_data_password(self):
		return self.password

	def correct_data_email(self):
		return self.email

	def correct_data_full_name(self):
		return self.full_name

	def incorrect_data(self):
		return ''

class LoginFormTest(TestCase):

	def test_witth_correct_data(self):
		form = LoginForm(initial={'username':username, 'password': password})
		self.assertTrue(form.is_bound)
		self.assertFalse(form.is_valid())

