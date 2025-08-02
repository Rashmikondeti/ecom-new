# base/forms.py
from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
    author = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Author name'
        })
    )
    category = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Category name'
        }),
        required=False  # Optional, depending on your model
    )

    class Meta:
        model = Book
        fields = ['title', 'description']  # Exclude 'author' and 'category' from Meta

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = ''

from django import forms
from .models import BookIssue

class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = ['user', 'book']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
        }
