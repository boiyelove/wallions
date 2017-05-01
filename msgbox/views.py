from django.shortcuts import render
from django.views.generic import View
from .models import UserMessage
from .forms import NewMessageForm

# Create your views here.

class MessageView(View):
	def get(self, request, receiver_uname):
		msgs = UserMessage.objects.get_conversation(sender = request.user, receiver=receiver_uname)
		template_name = messages.html
		context = {'user_msgs': msgs}
		return render(request, template, context)

	def post(self, request, receiver_id):
		form = NewMessageForm(request.POST or None)
		if form.is_bound and form.is_valid():
			text= form.cleaned_data.get('text')
			msg = UserMessage.objects.new_message(sender = request.user,
											receiver = receiver_uname,
											text = text)

		return self.get(request, receiver_uname)

class MessageList(View):
	def get(self, request):
		msg = UserMessage.objects.get_conversation_list(user = request.user)
		template = 'messages.html'
		context = {'user_msgs': msg}
		return render(request, template, context)
