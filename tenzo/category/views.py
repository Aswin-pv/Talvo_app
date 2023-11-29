from django.shortcuts import render,get_object_or_404
from .models import Category,Subcategory
from employee.models import Employee
from django.contrib.auth.decorators import login_required


@login_required
def category(request):
    categories = Category.objects.all()
    return render(request, "category/category.html", { 'categories' : categories })


def sub_category(request,slug):
    category = get_object_or_404(Category, slug=slug)
    sub_categories = Subcategory.objects.filter(category=category)
    return render(request, 'category/sub_category.html',{'sub_categories':sub_categories})


def employee_list(request, category_slug, sub_category_slug):
    
    return render(request, 'employee/employee_list.html')
