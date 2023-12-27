from django.db import models
from django.conf import settings
from category.models import Subcategory
import random



class Booking(models.Model):
    payment_mode_choice = (
        ('razorpay', 'Razorpay'),
        ('cash', 'Cash Payment'),
    )
    booking_statuses = (
        ('Pending','Pending'),
        ('Completed', 'Completed'),

    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='order_user')
    order_id = models.CharField(max_length=12,unique=True)
    fname = models.CharField(max_length=50, null=False)
    address1 = models.CharField(max_length=250,null=False,blank=False)
    address2 = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250,null=True)
    phone = models.CharField(max_length=10,null=False)
    state = models.CharField(max_length=100,null=False)
    pincode = models.CharField(max_length=6,null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    booking_date = models.DateField(null=False,blank=False)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    payment_mode = models.CharField(max_length=150,null=False,choices=payment_mode_choice,default='cash')
    razorpay_payment_id = models.CharField(max_length=100, null=True)
    razorpay_order_id = models.CharField(max_length=100, null=True)
    razorpay_signature = models.CharField(max_length=100, null=True)
    booking_status = models.CharField(max_length=150, choices=booking_statuses, default='Pending')
    billing_status = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)   
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ',k=8))
        super().save(*args, **kwargs)    
    
class BookedSubcategory(models.Model):
    booking = models.ForeignKey(Booking, related_name='subcategory', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,related_name='booked_subcategory', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
