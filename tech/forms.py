from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {'username': None,}


class UpdateProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, label='Profile Picture')
    first_name = forms.CharField(required=False, label='First Name')
    last_name = forms.CharField(required=False, label='Last Name')
    
    class Meta:
        model = Profile
        fields = ['profile_pic', 'first_name', 'last_name', 'bio']


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label='Email')
    subject = forms.CharField(required=True, label='Subject')
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'col': 'auto'}), 
        required=True, 
        label='Message',
    )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'image', 'content', 'tags']


"""
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="", 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here...', 'rows': '4', 'col': '50'})
    )
    class Meta:
        model = ForumComment
        fields = ('content',)


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'section', 'content']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'image', 'content']
"""