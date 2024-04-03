from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from .cart import Cart
from category.models import Subcategory
from .models import Booking,BookedSubcategory,Coupon,Coupon_Redeemed_Details
import razorpay
from django.conf import settings
from user.models import Address
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction

#-------------cart summary page views------------------

@login_required
def cart_summary(request):
    try:
        cart = Cart(request)

        cart_subcategory = cart.get_subcategory()   # Get the subcategories in cart
        quantities = cart.get_quantity()            # Get the quantities of subcategories in cart
        cart_quantities = len(cart)                 # Get the number of subcategories in cart

        # Total amount in cart
        total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)

        return render(request, 'cart/cart_summary.html', {'cart_subcategory': cart_subcategory, 'quantities': quantities, 'total': total_amount, 'cart_quantity': cart_quantities})

    except ObjectDoesNotExist:
        # Handle the case where a required object does not exist
        error_message = "Cart items not found"
        return render(request, 'cart/error.html', {'error_message': error_message})

    except Exception as e:
        # Handle other unexpected exceptions
        error_message = str(e)
        return render(request, 'cart/error.html', {'error_message': error_message})

def cart_add(request):

    try:
        cart = Cart(request)

        if request.method == 'POST' and request.POST.get('action') == 'post':
            subcategory_id = int(request.POST.get('subcategory_id'))
            subcategory_quantity = int(request.POST.get('sub_quantity'))

            # Retrieve the subcategory object
            subcategory = get_object_or_404(Subcategory, id=subcategory_id)

            # Add the subcategory to the cart
            cart.add(subcategory=subcategory, quantity=subcategory_quantity)

            # Get the updated cart quantity
            cart_quantity = len(cart)

            return JsonResponse({'qty': cart_quantity})

    except ValueError:
        # Handle invalid integer conversion
        return JsonResponse({'error': 'Invalid data format'}, status=400)

    except ValidationError:
        # Handle validation errors (e.g., if subcategory ID is invalid)
        return JsonResponse({'error': 'Validation error'}, status=400)

    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': str(e)}, status=500)


def cart_update(request):
    try:
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            subcategory_id = int(request.POST.get('subcategory_id'))
            subcategory_quantity = int(request.POST.get('sub_quantity'))

            # Update the cart with the provided subcategory and quantity
            cart.update(subcategory=subcategory_id, quantity=subcategory_quantity)

            # Retrieve updated cart details
            cart_subcategory = cart.get_subcategory()
            quantities = cart.get_quantity()

            # Calculate total amount in the cart
            total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
            cart_quantity = cart.__len__()
            response = JsonResponse({'qty': cart_quantity,'total':total_amount})
            return response
        
    except ValueError:
        # Handle invalid integer conversion
        return JsonResponse({'error': 'Invalid data format'}, status=400)

    except ObjectDoesNotExist:
        # Handle object not found (e.g., subcategory doesn't exist)
        return JsonResponse({'error': 'Subcategory not found'}, status=404)

    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': str(e)}, status=500)



def cart_delete(request):
    try:
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            #get the subcategory using subcategory_id
            subcategory_id = int(request.POST.get('subcategory_id'))
            subcategory = get_object_or_404(Subcategory,id=subcategory_id)

            #delete the subcategory using delete method
            cart.delete(subcategory=subcategory)

            # for finding total after removing a particular item from cart
            cart_subcategory = cart.get_subcategory()
            quantities = cart.get_quantity()
            total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)

            cart_quantity = cart.__len__()

            response = JsonResponse({'qty': cart_quantity,'total':total_amount})
            return response
        
    except ValueError:
    # Handle invalid integer conversion
        return JsonResponse({'error': 'Invalid data format'}, status=400)

    except ObjectDoesNotExist:
        # Handle object not found (e.g., subcategory doesn't exist)
        return JsonResponse({'error': 'Subcategory not found'}, status=404)

    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': str(e)}, status=500)

def clear_cart(request):
    
    cart = Cart(request)
    if cart:
        cart.clear()

    return redirect('cart:cart_summary')


#-------------checkout page views----------------

@login_required
def checkout_view(request):
   
    try:
        cart = Cart(request)
        cart_subcategory = cart.get_subcategory()
        quantities = cart.get_quantity()

        #If the cart is empty redirect to home
        if cart.__len__() <= 0:
            return redirect('home:home')


        try:
            #get the coupon object
            coupons = Coupon.objects.all()
        except Coupon.DoesNotExist:
            pass    

        #check if a coupon is stored in the session
        if 'coupon' in request.session:
            #if the coupon exist in session, clear it
            del request.session['coupon']    


        # Total amount in cart
        total_amount = sum(subcategory.charge * quantities[str(subcategory.id)] for subcategory in cart_subcategory)
        total_amount = float(total_amount)
        tax = (total_amount * 2) / 100
        grand_total = tax + total_amount

        #get the address which is selected by user
        address = Address.objects.filter(user=request.user, is_default=True).first()

        if address:
            with transaction.atomic():
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

                # Generate booking number and set as booking id
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr, mt, dt)
                current_date = d.strftime("%Y%m%d")
                booking_number = "#" + str(current_date) + ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))
                booking.order_id = booking_number

                booking.save()

                #Booking details for the specified category
                for subcategory in cart_subcategory:
                    BookedSubcategory.objects.create(
                        booking=booking,
                        subcategory=subcategory,
                        price=subcategory.charge,
                        quantity=max(quantities[str(subcategory.id)], 0)
                    )

            context = {
                'cart_subcategory': cart_subcategory,
                'quantities': quantities,
                'total': grand_total,
                'address': address,
                'tax': tax,
                'coupons': coupons,
                'booking_id': booking_number,
                'address': address,
            }
        else:
            context = {
                'cart_subcategory': cart_subcategory,
                'quantities': quantities,
                'address': address,
                'total': grand_total,
                'tax': tax,
                'coupons': coupons,
            }
        return render(request, 'cart/checkout.html', context=context)
    
    except Exception as e:
        # Handle the exception 
        error_message = f"An error occurred: {str(e)}"
        return render(request, 'cart/error.html', {'error_message': error_message})


@login_required
def cash_on_payment(request):

    try:
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            booking = get_object_or_404(Booking, order_id=booking_id)
            booking_date = request.POST.get('booking_date')
            payment_method = request.POST.get('payment_method')

            #check if the user select cash as payment method
            if payment_method == 'cash':
                booking.is_booked = True
                booking.booking_date = booking_date
                booking.payment_mode = payment_method

                booking.save()

                #if the coupon is applied save the coupon details
                if 'coupon' in request.session:
                    coupon_code = request.session.pop('coupon')
                    try:
                        coupon = Coupon.objects.get(coupon_code=coupon_code)
                        redeemed_details = Coupon_Redeemed_Details(user=request.user, coupon=coupon, is_redeemed=True)
                        redeemed_details.save()
                    except Coupon.DoesNotExist:
                        pass

                # Clear coupon from session after successful payment
                request.session.pop('coupon', None)        
     
                return JsonResponse({'success':True})
        
    except Exception as e:

        print(f"Error:{e}")

        return JsonResponse({'success':False})

@login_required
def razorpay_payment(request):
    try:
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            booking = get_object_or_404(Booking, order_id=booking_id)
            booking_date = request.POST.get('booking_date')
            payment_method = request.POST.get('payment_method')
            total = booking.grand_total
            
            #check if the user is selected razorpay as payment method
            if payment_method == 'razorpay':
                #razorpay logic
                client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
                client.set_app_details({"title" : "Django", "version" : "4.2.7"})
                        
                razorpay_total_amount = total*100     

                data = { "amount": razorpay_total_amount, "currency": "INR", "receipt": "order_rcptid_11" ,"partial_payment":False}

                payment = client.order.create(data=data)

                booking.razorpay_payment_id = payment['id']
                booking.booking_date = booking_date
                booking.payment_mode = payment_method
                booking.save()

                #if the coupon is applied save the coupon details
                if 'coupon' in request.session:
                    coupon_code = request.session.pop('coupon')
                    try:
                        coupon = Coupon.objects.get(coupon_code=coupon_code)
                        redeemed_details = Coupon_Redeemed_Details(user=request.user, coupon=coupon, is_redeemed=True)
                        redeemed_details.save()
                    except Coupon.DoesNotExist:
                        pass

                # Clear coupon from session after successful payment
                request.session.pop('coupon', None)  
                
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

@login_required
def booking_success(request):
    
    #Get the recent booking
    recent_booking = Booking.objects.filter(is_booked=True).order_by('-created').first()

    return render(request, 'cart/success_order.html',{'recent_item':recent_booking})
    
@login_required
def apply_coupon(request):   

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        booking_id = request.POST.get('booking_id')
        
        
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            booking = Booking.objects.get(order_id=booking_id)

            if 'coupon' in request.session:
                #If a coupon is already applied to the sesion
                return JsonResponse({'success':False,'error_message': 'Only on coupon can be applied'})

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

                        request.session['coupon'] = coupon_code

                        
                        return JsonResponse({'success':True, 'updated_total':updated_total,'coupon':coupon.coupon_code,'discount':coupon.discount_amount})
                else:
                    return JsonResponse({'success':False,'error_message': 'Coupon is not applicable for the order total'})

            else:
                return JsonResponse({'success':False,'error_message': 'Coupon is not applicable for the current date'})

        except Coupon.DoesNotExist:
            return JsonResponse({'success':False,'error_message': 'Invalid coupon code.'})     


def cancel_coupon(request):
        
    if request.method == 'POST':

        coupon_code = request.POST.get('coupon')
        booking_id = request.POST.get('booking_id')

        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            booking = Booking.objects.get(order_id=booking_id)

            #check if a coupon is stored in the session
            if 'coupon' in request.session:
                
                updated_total = booking.grand_total + float(coupon.discount_amount)
                booking.grand_total = updated_total
                booking.save()

                #if the coupon exist in session, clear it
                del request.session['coupon']  

                return JsonResponse({'success':True, 'updated_total':updated_total,})

        except Coupon.DoesNotExist:
            pass

        return JsonResponse({'success':True})        
    
   
    
@login_required
def payment_failed(request):
    
    return render(request, 'cart/payment_failed.html')



