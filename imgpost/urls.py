from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^upload/$', views.CreateImgPost.as_view(), name='upload-imgpost'),
	url(r'^p/(?P<pk>\d+)/$', views.ImgPostDetail.as_view(), name='detail-imgpost'),
	url(r'^p/(?P<pk>\d+)/edit/$', views.ImgPostEdit.as_view(), name='edit-imgpost'),
	url(r'^posts/$', views.ImgPostList.as_view(), name='list-imgpost'),
	url(r'^$', views.ImgPostList.as_view(), name='home'),

	]