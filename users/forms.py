from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم', widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="البريد الإلكتروني", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='الاسم الأول', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="الاسم الأخير", widget=forms.TextInput(attrs={"class": "form-control"}))


    class Meta:
        model = User 
        fields = ["username", 'first_name', 'last_name', 'email']

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile 
        fields = ['image']