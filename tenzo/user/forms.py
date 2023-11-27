from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email','phone_number']



class UserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username','email','phone_number','Address','street','city','state','pincode','date_of_birth','profile_picture']   
