from django.shortcuts import render
from .models import Category,Subcategory
from django.contrib.auth.decorators import login_required


@login_required
def category(request):
    categories = Category.objects.all()
    return render(request, "category/category.html", { 'categories' : categories })


def sub_category(request,pk):
    sub_categories = Subcategory.objects.filter(category_id=pk)
    return render(request, 'category/sub_category.html',{'sub_categories':sub_categories})
