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