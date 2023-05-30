from django import forms
from .models import Media, Post

from django.forms.models import inlineformset_factory


# from .forms import MediaForm


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['file']


#  include the MediaForm using formsets
MediaFormSet = inlineformset_factory(Post, Media, form=MediaForm, extra=1, can_delete=True)


class PostForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'caption'}),
                              required=False)
    tag = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}), required=False)

    class Meta:
        model = Post
        fields = ['caption', 'tags']


# class NewPostForm(forms.ModelForm):
#     picture = forms.ImageField(required=True)
#     caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'caption'}),
#                               required=False)
#     tag = forms.CharField(widget=forms.TextInput(
#         attrs={'class': 'input'}), required=False)
#
#     class Meta:
#         model = Post
#         fields = ['picture', 'caption', 'tags']
