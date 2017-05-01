from django.db import models
from django.db.models import F
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import send_mail
from webcore.models import TimestampedModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from imgpost.models import ImgPost
# Create your models here.


User = settings.AUTH_USER_MODEL


def user_directory_path(instance, filename):
	return 'uploads/user_{0}/{1}'.format(instance.user.id, filename)

class UserProfile(TimestampedModel):
	user = models.OneToOneField(User)
	headshot = models.ImageField(upload_to = user_directory_path)
	name = models.CharField(max_length = 60)
	bio = models.TextField(max_length = 320, null=True)
	verified = models.BooleanField(default = False)
	referral = models.ForeignKey(User, null=True, editable=False, related_name='parent')
	lastpasswordreset = models.DateTimeField(null=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	name  = models.CharField(max_length = 160)
	description = models.TextField()
	profile_bg =  models.ImageField(upload_to="user_profile")
	website = models.URLField()
	views = models.PositiveIntegerField(default = 0)
	follows = models.ManyToManyField('self', related_name='followers', symmetrical=False)
	blocks = models.ManyToManyField('self', related_name='blockedusers', symmetrical=True)

	def post_count(self):
		me = self.user
		post_count = ImgPost.objects.filter(author = me).count()
		return post_count


#Email Verification
class EmailVerification(TimestampedModel):
	email = models.EmailField(default = "example@domain.ext", unique=True)
	slug = models.SlugField(null = True)
	confirmed = models.BooleanField(default=False)
	action = models.URLField()
	actiontype = models.CharField(max_length = 10, default='USER')

	def __str__(self):
		return ('%s %s' % (self.email, self.confirmed))

	def send_activation_email(self):
		verification_url = "%s%s" % (settings.SITE_URL, 
			reverse_lazy('accounts:verify-email', kwargs={'verification_key':self.slug}))
		message = render_to_string("accounts/newsletter/verification_message.txt", {
			"website": settings.SITE_NAME,
			"verification_url": verification_url,
		})
		subject = "Verify your email"
		self.email_user(subject, message)

	def email_user(self, subject, message):
		send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])


class FavouriteItems(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	posts = models.ManyToManyField(ImgPost)


class Following(models.Model):
	user  = models.OneToOneField(settings.AUTH_USER_MODEL)
	users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followed_by")


class BlockedUser(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="blocked_userset" )
	users = models.ManyToManyField(settings.AUTH_USER_MODEL)