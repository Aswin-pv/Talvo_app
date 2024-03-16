from django.contrib import admin
from user.models import User
from .models import Contact

#Represent as table 
class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'email']

admin.site.register(User,UserAdmin)
admin.site.register(Contact)