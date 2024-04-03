from .cart import Cart

#create a context processors (Ensure our cart works on all pages of our website)
def cart(request):
    return {'cart': Cart(request)}

