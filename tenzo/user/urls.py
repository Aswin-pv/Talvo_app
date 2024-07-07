from django.urls import path
from . import views

urlpatterns = [
   path('',views.profile,name='profile'),
   path('update/<pk>',views.update_profile, name='update'),
   path('coupons/',views.coupons, name='coupons'),
   path('address/',views.address_list, name='address_list'),
   path('address/add',views.add_address, name='add_address'),
   path('address/edit/<int:pk>/',views.edit_address, name='edit_address'),
   path('address/delete/',views.delete_address, name='delete_address'),
   path('address/activate_address/',views.activate_address, name='activate_address'),
   path('bookings/',views.bookings, name='all_bookings'),
   path('pending/',views.pending_bookings, name='pending_bookings'),
   path('completed/',views.completed_bookings, name='completed_bookings'),
   path('cancelled/',views.cancelled_bookings, name='cancelled_bookings'),
   path('booking-details/<str:tracking_no>/',views.booking_details, name='booking_details'),
   path('invoice/<str:tracking_no>',views.invoice_view, name='invoice_view'),
   path('cancel-booking/<int:pk>/',views.cancel_booking, name='cancel_booking'),
]
