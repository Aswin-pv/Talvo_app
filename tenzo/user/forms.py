from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User

class UserRegisterForm(UserCreationForm):
    fname = forms.CharField(max_length=30, required=True)
    lname = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['fname','lname','username', 'email','phone_number']


class UserUpdateForm(UserChangeForm):
    class Meta:
        Model = User
        fields = ['fname','lname','username','email','phone_number','street','city','state','pincode','date_of_birth','profile_picture']        