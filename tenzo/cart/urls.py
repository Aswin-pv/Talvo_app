from django.urls import path,include
from . import views

app_name = 'cart'

urlpatterns = [
    path('',views.cart_summary, name='cart_summary'),
    path('add/',views.cart_add, name='cart_add'),
    path('delete/',views.cart_delete, name='cart_delete'),
    path('update/',views.cart_update, name='cart_update'),
    path('checkout/',views.checkout_view, name='checkout'),
    path('payment-success/',views.payment_success, name='payment-success'),
    path('payment-failed/',views.payment_failed, name='payment-failed')

]
