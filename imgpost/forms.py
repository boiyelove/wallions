from django import forms
from .models import ORIENTATION, ImgPost

class ImgPostForm(forms.Form):
	description = forms.CharField(widget=forms.TextInput)
	image = forms.ImageField()
	category_name = forms.ChoiceField(widget=forms.RadioSelect, choices = ORIENTATION)

	def __init__(self, *args, **kwargs):
		super(ImgPostForm, self).__init__(*args, **kwargs)
		self.fields['image'].widget.attrs = {'onchange':"preview_image(event)",'accept':"image/*" }
		self.fields['description'].widget.attrs = {'placeholder':"Description"}




	def done(self):
		image = self.cleaned_data.get('image')
		jimage = ImgPost.objects.create(
				orientation = self.cleaned_data.get('category_name'),
				description = self.cleaned_data.get('description'),
				imgurl = image)

		
			# obj = ImgPost.objects.create()
			# messages.success(request, 'Image was uplaoded successfully')
			# return obj.get_absolute_url