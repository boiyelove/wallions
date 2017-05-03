from django.conf.urls import url
from . import views


app_name="accounts"

urlpatterns = [
	url(r'^signin/$', views.LoginView.as_view(), name="login"),
	url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
	url(r'^signup/$', views.RegisterView.as_view(), name='register'),
	url(r'^ref/(?P<username>[\w-]+)/$', views.GetRef.as_view(), name='get-referral'),
	url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
	url(r'^profile/$', views.UserProfileView.as_view(), name='userprofile'),
	url(r'^verify_email/(?P<verification_key>[\w-]+)/$', views.EmailVerificationView.as_view(), name='verify-email'),
	url(r'^request_new_password/$', views.PasswordChangeRequestView.as_view(), name='password-request'),
	url(r'^change_password/$', views.PasswordChangeView.as_view(), name='password-change'),
]