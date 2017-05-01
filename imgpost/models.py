import os
from uuid import uuid4
from django.conf import settings
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType



class TimestampedModel(models.Model):
	created_on = models.DateTimeField(auto_now_add = True)
	updated_on = models.DateTimeField(auto_now = True)

	class Meta:
		abstract = True

ORIENTATION = (('Landscape','Landscape'),
				 ('Portrait','Portrait'),
				 ('Square','Square'))

def user_directory_path(instance, filename):
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}.{}'.format(instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)

	# return 'user_{0}uploads'.format(instance.id)
	return 'useruploads/{0}'.format(filename)

# Create your models here.
class TaggedItem(TimestampedModel):
	tag = models.SlugField()
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	def __str__(self):
		return self.tag
# post =  ImgPost(...)
# TaggedItem(content_object=post, tag="Tag-name")


class ImgPost(TimestampedModel):
	orientation = models.CharField(max_length = 160, choices=ORIENTATION)
	description = models.TextField(null=True)
	width = models.PositiveIntegerField(default=1, null=True)
	height = models.PositiveIntegerField(default=1, null=True)
	created = models.DateField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	views= models.PositiveIntegerField(default = 0, editable=False)
	downloads= models.PositiveIntegerField(default = 0, editable=False)
	imgurl = models.ImageField(upload_to=user_directory_path, width_field='width', height_field='height')
	user = models.ForeignKey(User)
	tags = GenericRelation(TaggedItem)

	def __str__(self):
		return str(self.id)

	def get_absolute_url(self):
		return reverse_lazy('detail-imgpost', kwargs={'pk': self.id})

	def dimension(self):
		return '{} x {}'.format(self.imgurl.width, self.imgurl.height)




@receiver(models.signals.pre_save, sender=ImgPost)
def auto_delete_file_on_change(sender, instance, **kwargs):
	if not instance.pk:
		return False
	try:
		old_file = ImgPost.objects.get(pk = instance.pk).imgurl
	except ImgPost.DoesNotExist:
		return False
	new_file = instance.imgurl
	if not old_file == new_file:
		try:
			if os.path.isfile(old_file.path):
				os.remove(old_file.path)
		except:
			return False

# @receiver(post_save, sender=ImgPost)
# def filefield_to_id(instance, created, **kwargs):
# 	if instance.id != instance.imgurl:
# 		print('Entered here')
# 		current = os.path.join(settings.MEDIA_ROOT ,str(instance.imgurl))
# 		new = os.path.join(settings.MEDIA_ROOT ,str(instance.id))
# 		newd = os.rename(current, new)
# 		instance.imgurl = newd
# 		print('out of here')
# 		instance.save()

@receiver(models.signals.post_delete, sender=ImgPost)
def deletefile(sender, instance, **kwargs):
	if instance.imgurl:
		if os.path.isfile(instance.imgurl.path):
			os.remove(instance.imgurl.path)