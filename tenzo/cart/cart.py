from category.models import Subcategory

class Cart():
    def __init__(self,request):
        self.session = request.session

        #Geting session key if exists
        cart = self.session.get('session_key')

        #if user is new Create new session key!
        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available on all pages
        self.cart = cart


    def add(self, subcategory,quantity):
        subcategory_id = str(subcategory.id)
        subcategory_quantity = str(quantity)

        if subcategory_id in self.cart:
            pass
        else:
            self.cart[subcategory_id] = int(subcategory_quantity) 

        self.session.modified = True    

    def update(self,subcategory,quantity):
        subcategory_id = str(subcategory)
        subcategory_quantity = int(quantity)

        cart = self.cart
        
        cart[subcategory_id] = subcategory_quantity

        self.session.modified = True
        cart = self.cart
        return cart
        

    def delete(self,subcategory):
        subcategory_id = str(subcategory.id)

        if subcategory_id in self.cart:
            del self.cart[subcategory_id]
            self.session.modified = True


    def __len__(self):
        return len(self.cart)       


    def get_subcategory(self):
        subcategory_ids = self.cart.keys()   

        subcategory = Subcategory.objects.filter(id__in=subcategory_ids)

        return subcategory
    
    def get_quantity(self):
        quantities = self.cart
        return quantities
    