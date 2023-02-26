from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Photo
        fields = ('file', )