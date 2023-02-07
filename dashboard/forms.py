from django.shortcuts import render,redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# class UserRegisterForm(UserCreationForm):
#     first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
#     last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
#     email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))

#     class Meta:
#         model = User
#         fields = ['username','first_name','last_name','email','password1','password2']