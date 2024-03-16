from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,HttpResponseServerError,HttpResponse
from .cart import Cart
from category.models import Subcategory
from .models import Booking,BookedSubcategory,Coupon,Coupon_Redeemed_Details
import razorpay
from django.conf import settings
from user.models import Address
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
from django.utils import timezone


def cart_summary(request):
    cart = Cart(request)
    cart_subcategory = cart.get_subcategory()
    quantities = cart.get_quantity() 
    cart_quantities = cart.__len__()  
    

    # Total amount in cart
    total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
    
    return render(request, 'cart/cart_summary.html',{'cart_subcategory':cart_subcategory,'quantities':quantities,'total':total_amount,'cart_quantity':cart_quantities})


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

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    print("Cart cleared succesfully")

    return redirect('cart:cart_summary')

def checkout_view(request):

    cart = Cart(request)
    cart_subcategory = cart.get_subcategory()
    quantities = cart.get_quantity() 

    if cart.__len__() <= 0:
        return redirect('home:home')

    coupons = Coupon.objects.all()

    # Total amount in cart
    total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
    total_amount = float(total_amount)
    tax = (total_amount * 2)/100
    grand_total = tax + total_amount
    

    address = Address.objects.filter(user=request.user, is_default=True).first()
    if address:
        booking = Booking()
        booking.user = request.user
        booking.fname = address.full_name
        booking.address1 = address.address1
        booking.address2 = address.address2
        booking.email = address.email
        booking.city = address.city
        booking.phone = address.phone
        booking.state = address.state
        booking.pincode = address.pincode
        booking.tax = tax
        booking.total_price = total_amount
        booking.grand_total = grand_total
        booking.ip = request.META.get('REMOTE_ADDR')
        print(booking.grand_total)

        #Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        booking_number ="#" + str(current_date) + ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ',k=6))
        booking.order_id = booking_number

        booking.save()

        for subcategory in cart_subcategory:
            BookedSubcategory.objects.create(
                    booking = booking,
                    subcategory = subcategory,
                    price = subcategory.charge,
                    quantity = max(quantities[str(subcategory.id)], 0)
                )

        context = {
            'cart_subcategory': cart_subcategory,
            'quantities': quantities,
            'total': grand_total,
            'address':address,
            'tax':tax,
            'coupons':coupons,
            'booking_id':booking_number,
        }
    else:
        context = {
            'cart_subcategory': cart_subcategory,
            'quantities': quantities,
            'address':address,
            'total': grand_total,
            'tax':tax,
            'coupons':coupons,
        }
        return render(request,'cart/checkout.html',context=context)        
    
    return render(request, 'cart/checkout.html',context=context)

def cash_on_payment(request):
    try:
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            booking = get_object_or_404(Booking, order_id=booking_id)
            booking_date = request.POST.get('booking_date')
            payment_method = request.POST.get('payment_method')

            if payment_method == 'cash':
                booking.is_booked = True
                booking.booking_date = booking_date
                booking.payment_mode = payment_method

                booking.save()

     
                return JsonResponse({'success':True})
        
    except Exception as e:

        print(f"Error:{e}")

        return JsonResponse({'success':False})

def razorpay_payment(request):
    try:
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            booking = get_object_or_404(Booking, order_id=booking_id)
            booking_date = request.POST.get('booking_date')
            payment_method = request.POST.get('payment_method')
            total = int(request.POST.get('total'))
            
            
            
            if payment_method == 'razorpay':
      
                client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
                client.set_app_details({"title" : "Django", "version" : "4.2.7"})
                        
                razorpay_total_amount = total*100     

                data = { "amount": razorpay_total_amount, "currency": "INR", "receipt": "order_rcptid_11" ,"partial_payment":False}

                payment = client.order.create(data=data)

                booking.razorpay_payment_id = payment['id']
                booking.booking_date = booking_date
                booking.payment_mode = payment_method
                booking.save()
                
                
                return JsonResponse({'success':True,'booking_id':payment})
        

    except Exception as e:
        
        print(f"Error:{e}")
            
        return JsonResponse({'success': False, 'error_message': 'An error occurred while processing the payment'})
    

@csrf_exempt
def razorpay_payment_complete(request):
    try:
        if request.method == 'POST':
            booking_id = request.POST.get('order_id')
            booking = get_object_or_404(Booking, razorpay_payment_id=booking_id)
            booking.billing_status = True
            booking.is_booked = True
            booking.save()
            return JsonResponse({'success':True})

    except Exception as e:

        print("Error",e)
        
        return JsonResponse({'status': 'error', 'message': 'Payment completion failed'})        
    

def apply_coupon(request):   

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        booking_id = request.POST.get('booking_id')
        print(booking_id)
        request.session['coupon'] = coupon_code
        

        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            booking = Booking.objects.get(order_id=booking_id)

            if coupon.valid_from <= timezone.now().date() <= coupon.valid_to:
                if booking.grand_total >= coupon.minimum_amount:
                    #check if the coupon is alredy redeemed by user
                    if coupon.is_redeemed_by_user(request.user):
                        return JsonResponse({'success':False,'error_message': 'The coupon is already redeemed by you'}) 
                    else:
                        #Apply the coupon and calculate the updated total
                        updated_total = booking.grand_total - float(coupon.discount_amount)
                        booking.grand_total = updated_total
                        booking.save()

                        #Mark the coupon as redeemed for user
                        redeemed_details = Coupon_Redeemed_Details(user=request.user, coupon=coupon, is_redeemed=True)
                        redeemed_details.save()
                        print(coupon.coupon_code)

                        return JsonResponse({'success':True, 'updated_total':updated_total,'coupon':coupon.coupon_code,'discount':coupon.discount_amount})
                else:
                    messages.error(request, 'Coupon is not applicable for the order total.')

            else:
                messages.error(request, 'Coupon is not applicable for the current date.')

        except Coupon.DoesNotExist:
            return JsonResponse({'success':False,'error_message': 'Invalid coupon code.'})     

    
           

def payment_failed(request):
    return render(request, 'cart/payment_failed.html')



