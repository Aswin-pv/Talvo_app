from django.shortcuts import render
from category.models import Category
from .models import Contact
from django.db import transaction

def home(request): 
    categories = Category.objects.all() #get all categories
    context = {
        'categories': categories,
    }
    return render(request, 'home/home.html', context=context)


def contact(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                contact = Contact()
                contact.full_name = request.POST.get('fullname')
                contact.email = request.POST.get('email')
                contact.phone_number = request.POST.get('phone')
                contact.message = request.POST.get('message')
                contact.save()
                return render(request, 'home/contact.html')
        except Exception as e:
            pass
    return render(request, 'home/contact.html')

            
    
  