from django.db import models
from user.models import User
from category.models import Subcategory



class Booking(models.Model):

    payment_mode_choice = (
        ('razorpay', 'Razorpay'),
        ('cash', 'Cash Payment'),
    )

    booking_statuses = (
        ('Pending','Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='order_user')
    is_booked = models.BooleanField(default=False)
    order_id = models.CharField(max_length=20,unique=True)
    fname = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250,null=True)
    city = models.CharField(max_length=250)
    phone = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    grand_total = models.FloatField()
    tax = models.FloatField()
    booking_date = models.DateField(null=True,blank=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    payment_mode = models.CharField(max_length=150,null=False,choices=payment_mode_choice,default='cash')
    razorpay_payment_id = models.CharField(max_length=100, null=True,blank=True)
    booking_status = models.CharField(max_length=150, choices=booking_statuses, default='Pending')
    billing_status = models.BooleanField(default=False)
    coupon_discount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    ip = models.CharField(max_length=20, blank=True)
    coupon_used = models.CharField(max_length=100,null=True,blank=True)


    class Meta:
        ordering = ('-is_booked','-created',)

    def __str__(self):
        return str(self.user)   
    
    def save(self, *args, **kwargs):

        # Check if the booking status is being changed to 'Completed' and payment method is not 'razorpay'
        if self.booking_status == 'Completed':
            self.billing_status = True 

        super().save(*args, **kwargs)    
    
class BookedSubcategory(models.Model):
    booking = models.ForeignKey(Booking, related_name='booking', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,related_name='booked_subcategory', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_amount = models.IntegerField(default=100)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def is_redeemed_by_user(self, user):
        redeemed_details = Coupon_Redeemed_Details.objects.filter(coupon=self, user=user, is_redeemed=True)
        return redeemed_details.exists()
    
    def __str__(self) -> str:
        return self.coupon_code
    


class Coupon_Redeemed_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_redeemed = models.BooleanField(default=False)