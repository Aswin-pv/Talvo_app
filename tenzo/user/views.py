from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserRegisterForm,UserUpdateForm,AddressForm
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user.models import User
from .models import Address


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



@login_required
def profile(request):
    users = User.objects.all()
    return render(request, 'user/profile.html', {'users': users} )     



def update_profile(request,pk):
    instance_to_be_edited = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance = instance_to_be_edited)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = UserUpdateForm(instance=instance_to_be_edited)

    return render(request, 'user/update_profile.html', { 'form' : form })        


#Address ahndling views

def add_address(request):
    if request.method == 'POST':
        print(request.user)
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('home:address_list')
    else:
        form = AddressForm()
    return render(request, 'user/add_address.html', {'form' : form})



def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'user/address_list.html', {'addresses':addresses})



def edit_address(request,pk):
    address = Address.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('home:address_list')
    else:
        form = AddressForm(instance=address)

    return render(request, 'user/edit_address.html',{'form':form})


def delete_address(request):
    print('staritng')
    if request.POST.get('action') == 'post':
        print("request accepted")
        address_id = int(request.POST.get('address_id'))
        address = get_object_or_404(Address, id=address_id)
        address.delete()
        return JsonResponse({'success':True})
    

def activate_address(request):
    print('starting')
    address_id = request.POST.get('address_id')
    Address.objects.update(is_default=False)
    Address.objects.filter(pk=address_id).update(is_default=True)

    return JsonResponse({'success': True})
