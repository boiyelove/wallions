import random
import hashlib
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import EmailVerification

def code_generator(codepulse):
	code = hashlib.sha1(str(random.random()).encode())
	code.update(codepulse.encode())
	code.update(str(datetime.utcnow()).encode())
	code = code.hexdigest()
	return code

def verify_email(email, actiontype=None, action='/'):
	emailverificationObj, created = EmailVerification.objects.get_or_create(email=email)
	if created:
		base, domain = str(email).split("@")
		code_exists = True
		while code_exists:
			verification_key = code_generator(base)[:10]
			code_exists = EmailVerification.objects.filter(slug = verification_key)
			if not code_exists:
				code_exists = False
		emailverificationObj.slug = verification_key
		if action:
			emailverificationObj.action = action
		if actiontype:
			emailverificationObj.actiontype = actiontype
		emailverificationObj.save()
		emailverificationObj.send_activation_email()


def email_password(user, password):
		message = render_to_string("accounts/newsletter/password_email.txt", {
			"website": settings.SITE_NAME,
			"password": password,
			'user': user,
		})
		subject = "Important Account Notice"
		send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
