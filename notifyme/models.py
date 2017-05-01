from django.db import models
from django.contrib.contentypes.fields import GenericForeignKey
from django.contrib.contentype.models import ContentType

# Create your models here.
class Notification(models.Model):
	action  = models.CharField(max_length = 160)
	url = models.URLField()
	read = models.BooleanField(deafault = False)


class ReportedItem(models.Model):
	action = models.CharField(max_length = 160)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')



class Notification(models.Model):
	sender_content_type = models.ForeignKey(ContentType, related_name='nofity_sender')
	sender_object_id = models.PositiveIntegerField()
	sender_object = GenericForeignKey("sender_content_type", "sender_object_id")
	
	verb = models.CharField(max_length=255)

	action_content_type = models.ForeignKey(ContentType, related_name='notify_action', 
		null=True, blank=True)
	action_object_id = models.PositiveIntegerField(null=True, blank=True)
	action_object = GenericForeignKey("action_content_type", "action_object_id")

	target_content_type = models.ForeignKey(ContentType, related_name='notify_target', 
		null=True, blank=True)
	target_object_id = models.PositiveIntegerField(null=True, blank=True)
	target_object = GenericForeignKey("target_content_type", "target_object_id")

	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
	read = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)