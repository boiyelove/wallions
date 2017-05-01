from django import forms


class NewMessageForm(forms.Form):
	text = forms.CharField(max_length = 320)