from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from .forms import ImgPostForm
from .models import ImgPost
from django.db.models import F
# Create your views herer

class CreateImgPost(FormView):
	form_class = ImgPostForm
	template_name = 'imgpost/upload.html'
	success_url = "/upload"


	def form_valid(self, form):
		form.done()
		return super(CreateImgPost, self).form_valid(form)

	def form_invalid(self, form):
		print('self is ', self)
		print('self.request.post is ', self.request.POST)
		print('self.form is ', form)
		print('error is', form.errors)
		return super(CreateImgPost, self).form_invalid(form)

class ImgPostEdit(View):
	def get(self, request, **kwargs):
		post = get_object_or_404(ImgPost, id=pk)
		form  = ImgPostForm(instance = post)
		return render(request, '', {'form': form})

	def post(self, request, **kwargs):
		imgform = ImgPostForm(request.POST or None)
		if imgform.is_bound and imgform.is_valid():
			obj = ImgPost.objects.create()
			messages.success(request, 'Image was uplaoded successfully')
			return obj.get_absolute_url
		return render(request, template, context)

class ImgPostList(View):
	def get(self, request, **kwargs):
		imgposts = ImgPost.objects.all()
		imgposts = Paginator(imgposts, 20)
		template = 'index.html'
		return render(request, template, {'posts': imgposts})

class ImgPostDetail(View):
	def get(self, request, **kwargs):
		pk = kwargs.pop('pk', None)
		post = get_object_or_404(ImgPost, id=pk)
		post.views = post.views + 1
		post.save()
		template = 'post.html'
		return render(request, template , {'post': post})

class ImgPostSearch(View):
	def get(self, request, **kwargs):
		sort_by = request.GET.get('sortb')
		filter_by = request.GET.get('filter')
		orientation = request.GET.get('orien')
		resolution = request.GET.get('resol')
		aspect_ratio = request.GET.get('aspec')
		s = request.GET.get('aspec')
		pass

