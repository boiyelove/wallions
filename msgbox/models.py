from itertools import chain
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
# Create your models here.



class MessageManager(models.Manager):

	def get_conversation(self, sender=None, receiver=None):
		q1 = Q(sender = sender)
		q11 = Q(receiver = receiver)
		q2 = Q(sender = sender)
		q21 = Q(receiver = receiver)
		msg = self.filter((q1 & q11) | (q2 & q21)).distinct().order_by('timestamp')
		return msg

	def new_message(self, sender, receiver, text):
		if sender and receiver:
			new_instance = self.create(sender = sender, receiver=receiver, text=text)
			return new_instance

	def get_conversation_list(self, user):
		q = Q(sender = user) | Q(receiver = user)
		msg = self.filter(q).order_by("-timestamp").distinct()
		l = []
		ulist =  User.objects.none()
		for m in msg:
			for u in m.receiver, m.sender:
				if u.username != user.username and u.username not in l: l.append(u.username)
		return l



class UserMessage(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'sender')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receipient')
	text  = models.CharField(max_length = 320)
	timestamp = models.DateTimeField(auto_now_add = True)
	updated_on = models.DateField(auto_now = True)
	active_for_sender = models.BooleanField(default = True)
	active_for_receipient = models.BooleanField(default = True)
	active = models.BooleanField(default=True)

	objects = MessageManager()

	def __str__(self):
		return self.text


	def from_me(self, me):
		if self.sender == me:
			return True
		return False