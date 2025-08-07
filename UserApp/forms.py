from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User, Article

class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'is_active')

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'is_published')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }