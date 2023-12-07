from django.contrib import admin
from . models import Category,Subcategory,Review

admin.site.register(Category)
admin.site.register(Subcategory)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('comment','rating','status','user','subcategory','created_date','updated_date')

admin.site.register(Review,ReviewAdmin)


