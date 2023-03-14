from django import forms
from userauth.models import Profile


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
                                 required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
                                required=False)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your biography'}),
                          required=False)
    url = forms.URLField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'url'}),
                         required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'location'}),
                               required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'bio', 'url', 'location']
