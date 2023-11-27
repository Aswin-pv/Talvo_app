from django.shortcuts import render
from .models import Category
from django.contrib.auth.decorators import login_required

@login_required
def category(request):
    categories = Category.objects.all()
    return render(request, "category/category.html", {'categories' : categories })
