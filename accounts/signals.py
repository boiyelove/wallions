from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from .models import UserProfile
from .utils import verify_email



@receiver(post_save, sender=User)
def verifyandcreateprofile(instance, created, sender, **kwargs):
	if created:
		up = UserProfile.objects.create(user = instance)
		if not instance.is_staff and settings.VERIFY_EMAILS:
			instance.is_active = False
			instance.save()
			verify_email(instance.email, action=reverse_lazy('accounts:userprofile'))




