from django import forms
from django.core.files.images import get_image_dimensions
from .models import ORIENTATION, ImgPost


class ImgPostForm(forms.Form):
	description = forms.CharField(widget=forms.TextInput)
	image = forms.ImageField()
	category_name = forms.ChoiceField(widget=forms.RadioSelect, choices = ORIENTATION)

	def __init__(self, *args, **kwargs):
		super(ImgPostForm, self).__init__(*args, **kwargs)
		self.fields['image'].widget.attrs = {'onchange':"preview_image(event)",'accept':"image/*" }
		self.fields['description'].widget.attrs = {'placeholder':"Description"}


	def clean_image(self):
		image = self.cleaned_data.get('image')
		width, height = get_image_dimensions(image)
		if width < 1000 or width > 10000 or height < 1000 or height > 10000:
			raise forms.ValidationError('Min Dimension is 1000x1000, Max Dimension is 10,000x10,000')


	def done(self):
		image = self.cleaned_data.get('image')
		jimage = ImgPost.objects.create(
				orientation = self.cleaned_data.get('category_name'),
				description = self.cleaned_data.get('description'),
				imgurl = image)

		
			# obj = ImgPost.objects.create()
			# messages.success(request, 'Image was uplaoded successfully')
			# return obj.get_absolute_url