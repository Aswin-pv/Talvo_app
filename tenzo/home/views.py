from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from category.models import Category
from .models import Contact

def home(request): 
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'home/home.html', context=context)


def contact(request):
    contact = Contact()
    if request.method == 'POST':
        print("running")
        contact.full_name = request.POST.get('fullname')
        contact.email = request.POST.get('email')
        contact.phone_number = request.POST.get('phone')
        contact.message = request.POST.get('message')
        contact.save()
        print("ending")

        
    return render(request, 'home/contact.html')

            
    
  