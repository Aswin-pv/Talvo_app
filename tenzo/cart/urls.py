from django.urls import path,include
from . import views

app_name = 'cart'

urlpatterns = [

    #cart summary page urls
    path('',views.cart_summary, name='cart_summary'),
    path('add/',views.cart_add, name='cart_add'),
    path('delete/',views.cart_delete, name='cart_delete'),
    path('update/',views.cart_update, name='cart_update'),
    path('clear/',views.clear_cart, name='cart_clear'),

    #checkout page urls
    path('checkout/',views.checkout_view, name='checkout'),
    path('apply-coupon/',views.apply_coupon, name='apply_coupon'),
    path('cancel-coupon/',views.cancel_coupon, name='cancel_coupon'),
    path('cash-on-payment/',views.cash_on_payment,name='cash_on_payment'),
    path('razorpay-payment/',views.razorpay_payment, name='razorpay_payment'),
    path('razorpay-payment-complete/',views.razorpay_payment_complete, name='razorpay_payment_complete'),
    path('success/',views.booking_success, name='success'),
    path('payment-failed/',views.payment_failed, name='payment-failed'),
]
