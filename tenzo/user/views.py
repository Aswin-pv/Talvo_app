from django.shortcuts import render,redirect
from .forms import UserRegisterForm,UserUpdateForm
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from user.models import User

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


def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = UserUpdateForm(instance=request.user)

    return render(request, 'user/update_profile.html', { 'form' : form })        


@login_required
def profile(request):
    users = User.objects.all()
    return render(request, 'user/profile.html', {'users': users} )            