from django.shortcuts import render
from django.http import JsonResponse
from category.models import Category
from .models import Contact
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def home(request): 

    categories = Category.objects.all() #get all categories

    # get recent categories exists in session
    recent_visits = request.session.get('recent_visits',[])
    recent_categories = Category.objects.filter(slug__in=recent_visits)
    recent_categories_len = len(recent_categories)

    context = {
        'categories': categories,
        'recent_categories':recent_categories,
        'recent_categories_len':recent_categories_len,
    }

    response =  render(request, 'home/home.html', context=context)
    return response

@login_required
def contact(request):
    if request.method == 'POST':
        try:
            #if any exception occurs before save or during save the transaction roll back
            with transaction.atomic():
                contact = Contact()
                contact.full_name = request.POST.get('fullname')
                contact.email = request.POST.get('email')
                contact.phone_number = request.POST.get('phone')
                contact.message = request.POST.get('message')
                contact.save()
                return JsonResponse({'success':True})
        except Exception as e:
            return JsonResponse({'success':False})
    return render(request, 'home/contact.html')

            
    
  