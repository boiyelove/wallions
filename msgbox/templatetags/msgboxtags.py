from django import template

register = template.Library()

@register.filter
def from_me(request, msg):
	if msg.sender == request.user:
		return True
	return False