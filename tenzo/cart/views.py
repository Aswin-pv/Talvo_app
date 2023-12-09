from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from category.models import Subcategory
# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_subcategory = cart.get_subcategory
    quantities = cart.get_quantity 
    return render(request, 'cart/cart_summary.html',{'cart_subcategory':cart_subcategory,'quantities':quantities})

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

def cart_delete(request):
    pass


def cart_update(request):
    pass