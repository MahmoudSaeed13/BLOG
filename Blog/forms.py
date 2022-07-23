from django import forms
from Blog.models import Category, Post, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',

        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',

        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',

        })
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
        })
    class Meta:
        fields = ['username','password']

class CreatePostForm(forms.ModelForm):
    image = forms.ImageField(label='post image', required=True)
    class Meta:
        model = Post
        fields = ['title', 'body', 'image','category']

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['title']