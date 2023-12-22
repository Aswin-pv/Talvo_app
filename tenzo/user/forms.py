from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User,Address

class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email','phone_number']

        
class UserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username','email','phone_number','profile_picture']   


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name','phone','address1','address2','city','state','pincode']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address1': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label=False)  
 