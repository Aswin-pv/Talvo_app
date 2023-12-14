from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from .cart import Cart
from category.models import Subcategory
import json


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

    return render(request, 'cart/checkout.html',{'cart_subcategory':cart_subcategory,'quantities':quantities,'total':total_amount})

