from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Image

class CustomUserCreationForm(UserCreationForm):
    # You can add fields from the CustomUser model here
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'description', 'category', 'image_file']
        widgets = {
            'category': forms.Select(),
            'image_file': forms.ClearableFileInput()
        }
