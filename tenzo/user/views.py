from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserRegisterForm,UserUpdateForm,AddressForm
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user.models import User
from .models import Address
from cart.models import Booking,BookedSubcategory
from cart.cart import Cart
import sweetify
from cart.models import Coupon,Coupon_Redeemed_Details


#Creating new user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            
            # shows a welcome message for the first login
            messages.success(request, f'Hey {username} , Welcome to Talvo')
            
            #Automatic login after account creation
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])  

            # if the newuser exists
            # return to home page
            if new_user is not None:
                login(request, new_user)  
                return redirect('home:home')
            else:
                # if newuser not exists or any login credential issuses return to login page
                return redirect('login')
        else:
            # Form is not valid, render the form with validation errors
            return render(request, 'user/sign-up.html', {'form': form})            

    else:
        form = UserRegisterForm()  
    return render(request, 'user/sign-up.html',context={ 'form' : form })



@login_required
def profile(request):
    return render(request, 'user/profile.html')     


#update the profile
def update_profile(request,pk):
    # get the user instance
    instance_to_be_edited = User.objects.get(pk=pk)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance = instance_to_be_edited)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Successfully Updated')
            return redirect('/profile/')
        else:
            pass
    else:
        form = UserUpdateForm(instance=instance_to_be_edited)

    return render(request, 'user/update_profile.html', { 'form' : form })        

def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'user/address_list.html', {'addresses':addresses})

#Address handling views
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            sweetify.success(request, 'New Address added')
            return redirect('home:address_list')
    else:
        form = AddressForm()
    return render(request, 'user/add_address.html', {'form' : form})


#Edit existing address
def edit_address(request,pk):

    address = get_object_or_404(Address, pk=pk)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Address Updated Successfully")
            return redirect('home:address_list')
        else:
            messages.error(request, "Invalid form creadentials !")
    else:
        form = AddressForm(instance=address)

    return render(request, 'user/edit_address.html',{'form':form})

#Remvoe address
def delete_address(request):
    
    if request.POST.get('action') == 'post':
        #get the address id
        address_id = int(request.POST.get('address_id'))
        address = get_object_or_404(Address, id=address_id)
        address.delete()
        return JsonResponse({'success':True})
    
#set the select address to default
def activate_address(request):
    #get the address id
    address_id = request.POST.get('address_id')
    #update all address's default to false
    Address.objects.update(is_default=False)
    #filter the selected address's default to true
    Address.objects.filter(pk=address_id).update(is_default=True)

    return JsonResponse({'success': True})


@login_required
def bookings(request):
    #filter the current user's bookings
    bookings = Booking.objects.filter(user=request.user, is_booked=True)
    
    
    context = {
       'bookings':bookings,
       'current_view': request.resolver_match.view_name
    }
    return render(request, 'user/bookings.html', context=context)

@login_required
def pending_bookings(request):
    #filter the current user's bookings
    bookings = Booking.objects.filter(user=request.user, is_booked=True, booking_status='Pending')
    
    
    context = {
       'bookings':bookings,
       'current_view': request.resolver_match.view_name
    }
    return render(request, 'user/bookings.html', context=context)

@login_required
def completed_bookings(request):
    #filter the current user's bookings
    bookings = Booking.objects.filter(user=request.user, is_booked=True, booking_status='Completed')
   
    
    context = {
       'bookings':bookings,
       'current_view': request.resolver_match.view_name
    }
    return render(request, 'user/bookings.html', context=context)

@login_required
def cancelled_bookings(request):
    #filter the current user's bookings
    bookings = Booking.objects.filter(user=request.user, is_booked=True, booking_status='Cancelled')

    
    context = {
       'bookings':bookings,
       'current_view': request.resolver_match.view_name
    }
    return render(request, 'user/bookings.html', context=context)

#Manage bookings
def booking_details(request,tracking_no):
    
    cart = Cart(request)
    cart_subcategory = cart.get_subcategory()
    quantities = cart.get_quantity() 

    # Total amount in cart
    total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
    total_amount = int(total_amount)
    
    bookings = Booking.objects.filter(order_id=tracking_no).filter(user=request.user).first()

    booking_subcategory = BookedSubcategory.objects.filter(booking=bookings)

    context = {
        'bookings':bookings,
        'booking_subcategory':booking_subcategory,
        'total' : total_amount,
    }

    return render(request, 'user/booking_detail.html',context=context)


def invoice_view(request,tracking_no):

    cart = Cart(request)
    cart_subcategory = cart.get_subcategory()
    quantities = cart.get_quantity() 

    # Total amount in cart
    total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
    total_amount = int(total_amount)

    bookings = Booking.objects.filter(order_id=tracking_no).filter(user=request.user).first()
    booking_subcategory = BookedSubcategory.objects.filter(booking=bookings)

    context = {
        'bookings':bookings,
        'booking_subcategory':booking_subcategory,
        'total' : total_amount,
        
    }

    return render(request, 'cart/invoice.html', context=context)


def cancel_booking(request,pk):
    
    booking = get_object_or_404(Booking, pk=pk)
    if booking:
        booking.booking_status = 'Cancelled'
        booking.save()
    else:
        sweetify.error(request, "Something went wrong")    

    return redirect('home:all_bookings')

    

def coupons(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons':coupons,
    }
    return render(request, 'user/coupons.html',context=context)