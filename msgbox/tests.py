from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import UserMessage
from selenium import webdriver
from django.core.urlresolvers import resolve
from .views import MessageList

# Create your tests here.
text = "Something like this and something like that"
text1 = "Something like this and that"
text2 = "Something like that this and"
text3 = "Something like this and something that like"

class UserMessageTest(TestCase):
	def setUp(self):
		self.user_a = User.objects.create_user(username='test_paul',  email='test_paul@example.com', password='t3stpassw0rd')
		self.user_b = User.objects.create_user(username='test_maurice',  email='test_maurice@example.com', password='t3stpassw0rd')

	def test_new_message_manager(self):
		msg = UserMessage.objects.new_message(sender = self.user_a, receiver = self.user_b, text=text)
		self.assertEqual(msg.text, text)
		self.assertEqual(self.user_a, msg.sender)
		self.assertEqual(self.user_b, msg.receiver)


	def test_get_conversation(self):
		msg = UserMessage.objects.new_message(sender = self.user_a, receiver = self.user_b, text=text)
		msg1 = UserMessage.objects.new_message(sender = self.user_a, receiver = self.user_b, text=text1)
		msg2 = UserMessage.objects.new_message(sender = self.user_a, receiver = self.user_b, text=text2)
		msg3 = UserMessage.objects.new_message(sender = self.user_a, receiver = self.user_b, text=text3)
		msgs = UserMessage.objects.get_conversation(sender=self.user_a, receiver=self.user_b)
		self.assertEqual(4, msgs.count())

	def test_get_conversation_list(self):
		msg = UserMessage.objects.new_message(sender = self.user_a, receiver = self.user_b, text=text)
		msg1 = UserMessage.objects.new_message(sender = self.user_b, receiver = self.user_a, text=text1)
		msg2 = UserMessage.objects.new_message(sender = self.user_a, receiver = self.user_b, text=text2)
		msg3 = UserMessage.objects.new_message(sender = self.user_b, receiver = self.user_a, text=text3)
		msgs = UserMessage.objects.get_conversation_list(user=self.user_a)
		self.assertEqual(1, len(msgs))
		self.assertTrue(list is type(msgs))


# class VisitorTest(TestCase):

# 	def setUp(self):
# 		self.browser = webdriver.Chrome(executable_path="C:\\tools\\chromedriver_win32\\chromedriver.exe")
# 		self.browser.implicitly_wait(3)

# 	def tearDown(self):
# 		self.browser.quit()

# 	def test_server_is_up(self):
# 		self.browser.get('http://localhost:8000')
# 		self.assertIn('Django', self.browser.title)

class MessageViewTest(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.user_a = User.objects.create_user(username='test_paul1',  email='test_paul1@example.com', password='t3stpassw0rd')
		

	def test_root_conf_resolves_to_message_view(self):
		request = self.factory.get('messages/')
		request.user = self.user_a
		response = MessageList.as_view()(request)
		self.assertEqual(response.status_code, 200)