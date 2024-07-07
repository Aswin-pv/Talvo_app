from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import *


class CouponRedeemedAdmin(admin.ModelAdmin):

    list_display = ['user', 'coupon']

class BookingAdmin(admin.ModelAdmin):

    list_display = ['order_id', 'user', 'is_booked', 'booking_date', 'booking_status' ,'billing_status', 'payment_mode']


admin.site.register(Booking,BookingAdmin)
admin.site.register(BookedSubcategory)
admin.site.register(Coupon)
admin.site.register(Coupon_Redeemed_Details,CouponRedeemedAdmin)

