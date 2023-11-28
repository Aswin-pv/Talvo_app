from django.shortcuts import render
from .models import Subcategory


def sub_category(request,pk):
    sub_categories = Subcategory.objects.filter(category_id=pk)
    return render(request, 'category/sub_category.html',{'sub_categories':sub_categories})
