from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.contrib.auth.models import AbstractUser


#Custom user model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(
        # mandate phone no to 10 digits
        max_length=10,
        validators=[
            MinLengthValidator(10, message="Phone number must be exactly 10 characters."),
            MaxLengthValidator(10, message="Phone number must be exactly 10 characters.")
        ],
        null=False
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    Address = models.CharField(max_length=255,null=True,blank=True)
    street = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255, null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    pincode = models.CharField(max_length=255,null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    #uses email as an authentification 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username

