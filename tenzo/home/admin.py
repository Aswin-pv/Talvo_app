from django.contrib import admin
from user.models import User

#Represent as table 
class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'email']

admin.site.register(User,UserAdmin)