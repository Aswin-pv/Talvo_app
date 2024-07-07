from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User,Address
from django.contrib.auth.forms import PasswordResetForm

# built-in usercreationform is used
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','phone_number']


# built-in userchangeform is used
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','email','phone_number','profile_picture']   

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name','phone','email','address1','address2','city','state','pincode']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address1': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
        }


# change password forms

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )