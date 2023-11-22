from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login,authenticate

#Creating new user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Hey {username} welcome to Talvo')
            #Automatic login after account creation
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])  
            login(request,new_user)  
            return redirect('home:home')
    else:
        form = UserRegisterForm()
            
        
    return render(request, 'user/sign-up.html',context={ 'form' : form })