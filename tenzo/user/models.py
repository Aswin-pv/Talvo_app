from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser


#Custom user model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10,validators=[validators.MaxLengthValidator(10)],null=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    street = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255, null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    pincode = models.CharField(max_length=255,null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username
    