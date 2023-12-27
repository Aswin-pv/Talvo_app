from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,HttpResponseServerError,HttpResponse
from .cart import Cart
from category.models import Subcategory
from .models import Booking,BookedSubcategory
import razorpay
from django.conf import settings
from user.models import Address
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_subcategory = cart.get_subcategory()
    quantities = cart.get_quantity() 

    # Total amount in cart
    total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
    
    return render(request, 'cart/cart_summary.html',{'cart_subcategory':cart_subcategory,'quantities':quantities,'total':total_amount})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        subcategory_id = int(request.POST.get('subcategory_id'))
        subcategory_quantity = int(request.POST.get('sub_quantity'))

        subcategory = get_object_or_404(Subcategory,id=subcategory_id)

        cart.add(subcategory=subcategory,quantity=subcategory_quantity)

        # get cart quantity
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty':cart_quantity})
        return response

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        subcategory_id = int(request.POST.get('subcategory_id'))
        subcategory_quantity = int(request.POST.get('sub_quantity'))

        cart.update(subcategory=subcategory_id, quantity=subcategory_quantity)

        cart_subcategory = cart.get_subcategory()
        quantities = cart.get_quantity()

        total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity,'total':total_amount})
        return response


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        subcategory_id = int(request.POST.get('subcategory_id'))
        subcategory = get_object_or_404(Subcategory,id=subcategory_id)
        cart.delete(subcategory=subcategory)

        # for finding total after removing a particular item from cart
        cart_subcategory = cart.get_subcategory()
        quantities = cart.get_quantity()

        total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)

        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity,'total':total_amount})
        return response


def checkout_view(request):

    cart = Cart(request)
    cart_subcategory = cart.get_subcategory()
    quantities = cart.get_quantity() 

    # Total amount in cart
    total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
    total_amount = int(total_amount)

    
    address = Address.objects.filter(user=request.user, is_default=True).first()
    booking = Booking()
    
    if request.method == 'POST':
        
        booking_date = request.POST.get('booking_date')
        payment_method = request.POST.get('payment_method')
        booking.user = request.user
        booking.fname = address.full_name
        booking.address1 = address.address1
        booking.address2 = address.address2
        booking.city = address.city
        booking.phone = address.phone
        booking.state = address.state
        booking.pincode = address.pincode
        booking.booking_date = booking_date
        booking.total_price = total_amount
        booking.payment_mode = payment_method

        booking.save()

        print('saved successfully')

        for subcategory in cart_subcategory:
            BookedSubcategory.objects.create(
                    booking = booking,
                    subcategory = subcategory,
                    price = subcategory.charge,
                    quantity = quantities[str(subcategory.id)]
                )

        if payment_method == 'cash':
            booking.booking_status = 'Completed'
            booking.save()
              
            return JsonResponse({'success':True})
        
        elif payment_method == 'razorpay':
            print("razorpay backend running")
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            client.set_app_details({"title" : "Django", "version" : "4.2.7"})
            
            total_amount = total_amount*100     

            data = { "amount": total_amount, "currency": "INR", "receipt": "order_rcptid_11" ,"partial_payment":False}

            payment = client.order.create(data=data)

            booking.razorpay_order_id = payment['id']

            print("*********")
            print(payment)
            print("*********")

            
            

            return JsonResponse({'booking_id':payment})
            
    context = {
        'cart_subcategory': cart_subcategory,
        'quantities': quantities,
        'total': total_amount,
        'address':address,
    }    
    
    return render(request, 'cart/checkout.html',context=context)
    

def place_order(request):
    cart = Cart(request)
    cart_subcategory = cart.get_subcategory()
    quantities = cart.get_quantity() 

    # Total amount in cart
    total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
    total_amount = int(total_amount)

    booking = Booking()

    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        payment_method = request.POST.get('payment_method')
        print("placeorder runnning")
        booking.booking_date = booking_date
        booking.booking_status = 'Complete'
        booking.save()

        context = {
        'cart_subcategory': cart_subcategory,
        'quantities': quantities,
        'total': total_amount,
    } 
    
    return render(request, 'cart/payment_completed.html', context=context)
                



def payment_success(request):

    cart = Cart(request)
    cart_subcategory = cart.get_subcategory()
    quantities = cart.get_quantity()

    context = {
        'cart_subcategory':cart_subcategory,
        'quantities':quantities,
    }

    return render(request, 'cart/payment_completed.html', context=context)


def payment_failed(request):
    return render(request, 'cart/payment_failed.html')



