from category.models import Subcategory
from django.core.exceptions import ObjectDoesNotExist

# we created session to store the cart items
class Cart():
    def __init__(self,request):
        self.session = request.session

        #Getting session key if exists
        cart = self.session.get('session_key')

        #if user is new Create new session key!
        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available on all pages of site
        self.cart = cart


    #add new subcategories to cart
    def add(self, subcategory,quantity):
        #retreive the data from cart_add view function
        subcategory_id = str(subcategory.id)
        subcategory_quantity = str(quantity) 
        

        #if subcategory_id in already in cart pass, else create a new session_key:value pair
        if subcategory_id in self.cart:
            # Update quantity if subcategory is already in cart
            self.cart[subcategory_id] += int(subcategory_quantity)
        else:
            # Add new subcategory to cart
            self.cart[subcategory_id] = int(subcategory_quantity) 

        self.session.modified = True    #To ensure that changes to session data are saved reliably

    #used to display the subcategory in cart
    def get_subcategory(self):
        subcategory_ids = self.cart.keys()   #dict_keys(['1', '2', '3'])
        
        #if the subcategory is in subcategory_ids, then get the subcategory and return
        subcategory = Subcategory.objects.filter(id__in=subcategory_ids)
        return subcategory    

    def update(self,subcategory,quantity):
        subcategory_id = str(subcategory)
        subcategory_quantity = int(quantity)

        # Check if subcategory_id is valid
        try:
            Subcategory.objects.get(id=subcategory_id)
        except ObjectDoesNotExist:
            raise ValueError('Invalid Subcategory ID')

        # Check if quantity is a valid integer
        if subcategory_quantity <= 0:
            raise ValueError('Quantity must be a positive integer')

        # Update quantity for the subcategory
        self.cart[subcategory_id] = subcategory_quantity
        self.session.modified = True
    

    def delete(self,subcategory):
        subcategory_id = str(subcategory.id)

        if subcategory_id in self.cart:
            del self.cart[subcategory_id]
            self.session.modified = True

    def clear(self):
        
        # Clear the cart (remove all items)
        self.cart = {}

        # Update the session with the modified cart
        self.session['session_key'] = self.cart
        self.session.modified = True

    #To get the total number of subcategories in cart 
    def __len__(self):
        return len(self.cart)       


    def get_quantity(self):
        quantities = self.cart
        return quantities
    