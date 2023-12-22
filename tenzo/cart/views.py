from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,HttpResponseServerError,HttpResponse
from .cart import Cart
from category.models import Subcategory
from .models import Booking,BookedSubcategory
import razorpay
from django.conf import settings
from .forms import BookingForm
from user.forms import CouponApplyForm
from user.models import Coupon



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
    print(total_amount)

    coupon_form = CouponApplyForm()

    
    if request.method == 'POST':
            print('Form submitted via post request')

            form = BookingForm(request.POST)
            if form.is_valid():
                print("validation is successfull")
                booking = form.save(commit=False)
                booking.user = request.user
                booking.total_price = total_amount
                booking.booking_status = 'Completed'

                booking.save()

                for subcategory in cart_subcategory:
                    BookedSubcategory.objects.create(
                        booking = booking,
                        subcategory = subcategory,
                        price = subcategory.charge,
                        quantity=quantities[str(subcategory.id)]
                    )

                payment_mode = request.POST.get('payment_mode')

                if payment_mode == 'razorpay':
                        
                    print("started if razorpay mode")
                    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
                    client.set_app_details({"title" : "Django", "version" : "4.2.7"})

                    
                    data = { "amount": total_amount, "currency": "INR", "receipt": "order_rcptid_11" ,"partial_payment":False}

                    payment = client.order.create(data=data)


                    print("*********")
                    print(payment)
                    print("*********")

                    

                    booking.status = 'completed'  # Update with your actual status
                    booking.save()

                    context = {
                        'form':form,
                        'cart_subcategory':cart_subcategory,
                        'quantities':quantities,
                        'payment':payment,

                    }
                    return render(request, 'cart/payment_completed.html',context=context)
                
                else:
                    context = {
                        'cart_subcategory':cart_subcategory,
                        'quantities':quantities,
                        'total_amount':total_amount,

                    }
                    return render(request, 'cart/payment_completed.html',context=context)

            else:
                print("INVALID FORM",form.errors)

    else:
        form = BookingForm()        


    context = {
        'form':form,
        'cart_subcategory': cart_subcategory,
        'quantities': quantities,
        'total': total_amount,
        'coupon_form':coupon_form,
    }    
    
    return render(request, 'cart/checkout.html',context=context)
    


                




# def place_order(request):
    
#     return render(request, '/')   

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



