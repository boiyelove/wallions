from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^messages/$', views.MessageList.as_view(), name='message-list'),
	url(r'^messages/(?P<receiver_id>\d+)/$', views.MessageView.as_view(), name='create-newmessage'),
	]