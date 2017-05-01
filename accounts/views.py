import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.views.generic import TemplateView, ListView
from django.views.generic.base import View
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from .forms import LoginForm, RegisterForm, UserProfileForm, PasswordRequestForm, PasswordChangeForm
from .models import UserProfile, EmailVerification
from django.contrib.auth.mixins import LoginRequiredMixin


class FormLink:
	def __init__(self, text, url):
		self.name = text
		self.url = url

	def __str__(self):
		return self.name


# Create your views here.
class LoginRqMixin(LoginRequiredMixin):
	login_url = reverse_lazy('accounts:login')
	redirect_field_name = 'rdr_to'



class AlreadyLoginedIn:

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return HttpResponseRedirect(reverse_lazy('accounts:dashboard'))
		else:
			return super(AlreadyLoginedIn, self).dispatch(*args, **kwargs)


# class MustBeProfiled:
# 	def dispatch(self, *args, **kwargs):
# 		dm = DonateMethod.objects.filter(user = self.request.user)
# 		up = UserProfile.objects.get(user=self.request.user)
# 		if not dm:
# 			messages.add_message(self.request, messages.INFO, 'Please add a way to recieve payment before you continue')
# 			return HttpResponseRedirect(reverse_lazy('accounts:donatemethod-create'))
# 		elif not up.phone_number or not up.full_name:
# 			messages.add_message(self.request, messages.INFO, 'Please complete your profile information before you continue')
# 			return HttpResponseRedirect(reverse_lazy('accounts:userprofile'))
# 		else:
# 			return super(MustBeProfiled, self).dispatch(*args, **kwargs)

class LoginView(AlreadyLoginedIn, FormView):
	form_class = LoginForm
	template_name = 'accounts/form.html'
	success_url = reverse_lazy('accounts:dashboard')

	def get_context_data(self, *args, **kwargs):
		formlinks = [FormLink("I don't have a revenupa account", reverse_lazy('accounts:register')),
		]
		context = super(LoginView, self).get_context_data(*args, **kwargs)
		context.update({'page_title' : 'Login',
		'form_title': 'Login',
		"form_action": reverse_lazy('accounts:login'),
		"form_method": "post",
		"form_value": "Take me to my account",
		'form_cancel': FormLink('I forgot my password', reverse_lazy('accounts:password-request')),
		'form_links': formlinks,
		})
		return context


	def form_valid(self, form):
		form.login_user(self.request)
		messages.success(self.request, 'You are now logged in')
		return super(LoginView, self).form_valid(form)


class LogoutView(LoginRqMixin, View):

	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, 'You are now logged out')
		return HttpResponseRedirect('/')


class RegisterView(FormView):
	form_class = RegisterForm
	template_name = 'accounts/form.html'
	success_url = reverse_lazy('accounts:login')

	# def dispatch(self, *args, **kwargs):
	# 	if request.is_authenticated:
	# 		return HttpResponseRedirect(reverse_lazy('accounts:dashboard'))
	# 	super(RegisterView, self)


	def get_context_data(self, *args, **kwargs):
		formlinks = [FormLink('Take me to revenupa.org', reverse_lazy('webcore:home-page')),]
		context = super(RegisterView, self).get_context_data(*args, **kwargs)
		context.update({'page_title' : 'Register New Account',
			'form_title' : 'Create New Account',
			'form_method': 'POST',
			'form_value': 'Create my revenupa account',
			'form_action': reverse_lazy('accounts:register'),
			'form_cancel': FormLink("I already have a revenupa account", reverse_lazy('accounts:login')),
			'form_links': formlinks,
			})
		return context

	def form_valid(self, form):
		referral = self.request.COOKIES.get('referral_id')
		form.register_user(referral)
		messages.add_message(self.request, messages.SUCCESS, 'Registration successful')
		messages.add_message(self.request, messages.INFO, 'An email has been sent to your email address, you can check your spam folder or wait a few minute to receive it')
		return super(RegisterView, self).form_valid(form)


class DashboardView(LoginRqMixin, TemplateView):
	template_name = "accounts/dashboard.html"

	def get_context_data(self, **kwargs):
		context = super(DashboardView, self).get_context_data(**kwargs)
		context['page_title'] = "Dashboard"
		context['balance'] = UserToken.objects.get(user = self.request.user)
		profile = UserProfile.objects.get(user = self.request.user)
		context['programs'] = profile.programs.all()
		return context


class UserProfileView(LoginRqMixin, UpdateView):
	form_class = UserProfileForm
	success_url = reverse_lazy('accounts:userprofile')
	template_name = 'settings.html'

	def get_context_data(self, *args, **kwargs):
		new_context = {'page_title' : 'My Profile',
		'form_title': 'Profile',
		"form_action": reverse_lazy('accounts:userprofile'),
		"form_method": "post",
		"form_value": "Update Profile",
		'error_message': "Please check the details you provided",
		}
		context = super(UserProfileView, self).get_context_data(*args, **kwargs)
		context.update(new_context)
		return context

	def get_object(self, *args, **kwargs):
		instance, created = UserProfile.objects.get_or_create(user = self.request.user)
		return instance

class GetRef(AlreadyLoginedIn, View):
	def get(self, request, *args, **kwargs):
		response = HttpResponseRedirect(reverse_lazy('accounts:register'), request)
		try:
			uname = kwargs.pop('username')
			user = User.objects.get(username = uname)
			response.set_cookie('referral_id', user, expires=datetime.date.today() + datetime.timedelta(days=360))
			messages.add_message(request, messages.SUCCESS, 'We commend {} for telling you about us. You are welcome'.format(uname))
		except:
			messages.add_message(request, messages.ERROR, 'Sorry, no user with that username')
		return response

class EmailVerificationView(View):
	def get(self, request, *args, **kwargs):
		kw = kwargs.pop('verification_key')
		try:
			emver = EmailVerification.objects.get(slug = kw)
			emver.confirmed = True
			messages.add_message(request, messages.SUCCESS, 'Your email has been confirmed successfully')
			if emver.actiontype == 'USER':
				try:
					user = User.objects.get(email = emver.email)
					if not user.is_active:
						user.is_active = True
						user.save()
						messages.add_message(request, messages.SUCCESS, 'Your account has been activated successfully')
				except:
					pass
			return HttpResponseRedirect(emver.action, request)
		except:
			raise Http404


class PasswordChangeRequestView(FormView):
	form_class = PasswordRequestForm
	template_name = "accounts/form.html"
	success_url = reverse_lazy('accounts:dashboard')

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse_lazy('accounts:password-change'))
		else:
			return super(PasswordChangeRequestView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.done()
		messages.add_message(self.request, messages.SUCCESS, 'An email containing your password was sent to your email address')
		return super(PasswordChangeRequestView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		formlinks = [FormLink('Take me to revenupa.org', reverse_lazy('webcore:home-page')),]
		new_context = {'page_title' : 'Password Recovery Request',
		'form_title': 'Password Recovery Request',
		"form_action": reverse_lazy('accounts:password-request'),
		"form_method": "post",
		"form_value": "Reset my password",
		'error_message': "Please check the details you provided",
		'form_cancel': FormLink("I remember my password", reverse_lazy('accounts:login')),
		'form_links': formlinks,
		}
		context = super(PasswordChangeRequestView, self).get_context_data(*args, **kwargs)
		context.update(new_context)
		return context

class PasswordChangeView(LoginRqMixin, FormView):
	form_class = PasswordChangeForm
	template_name = "accounts/form.html"
	success_url = reverse_lazy('accounts:dashboard')

	def form_valid(self, form):
		form.done()
		'An email containing your password was sent to your email address'
		messages.add_message(self.request, messages.SUCCESS, 'Your password as been changed and emailed to you')
		return super(PasswordChangeView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(PasswordChangeView, self).get_form_kwargs()
		kwargs['request'] = self.request
		print('when through here')
		return kwargs

	def get_context_data(self, *args, **kwargs):
		formlinks = [FormLink('Take me to my profile', reverse_lazy('accounts:userprofile')),]
		new_context = {'page_title' : 'Password Change Form',
		'form_title': 'Password Change Form',
		"form_action": reverse_lazy('accounts:password-change'),
		"form_method": "post",
		"form_value": "Change my password",
		'error_message': "Please check the details you provided",
		'form_cancel': FormLink("Nah, take me to dashboard", reverse_lazy('accounts:dashboard')),
		'form_links': formlinks,
		}
		context = super(PasswordChangeView, self).get_context_data(*args, **kwargs)
		context.update(new_context)
		return context


class SearchView(View):
	def get(self, request, *args, **kwargs):
		search = kwargs.get('search', None)


		'''Search Queries goes here'''


		template = 'search.html'
		return render(request, template, context)