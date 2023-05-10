from django import forms
from post.models import Post


class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'caption'}), required=False)
    tag = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}), required=False)

    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tags']

