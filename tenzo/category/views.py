from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Subcategory,Review
from cart.models import Booking,BookedSubcategory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm
from django.http import JsonResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.template.loader import render_to_string
from django.db import DatabaseError
import sweetify

#all services category
@login_required
def category(request):
    try:
        categories = Category.objects.all()      # to get all the categories

        if not categories.exists():
            # If no categories are found, send a message and render the template
            messages.info(request, 'Sorry ! No services available at the moment')
            return render(request, "category/category.html")

        # paginator for displaying multiple pages
        paginator = Paginator(categories,2)
        page_number = request.GET.get('page')       # retrieves the value associated with the key 'page' from the query parameters.
        try:
            categoryfinal = paginator.get_page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            categoryfinal = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver the last page of results.
            categoryfinal = paginator.page(paginator.num_pages)

        total_pages = categoryfinal.paginator.num_pages

        context = {
            'categoryfinal' : categoryfinal,
            'last_page': total_pages,
            'totalpagelist': [n+1 for n in range(total_pages)],
        }

        return render(request, "category/category.html", context=context)
    except Exception as e:
       
        messages.error(request, 'An error occurred while fetching the categories.')
        return render(request, "category/category.html")

#For autocomplete of category search
def search_list(request):  
    try:    
        # retrieves a list of values for the title field
        category = Category.objects.filter().values_list('title', flat=True)  #gives a flat list rather than the tuples
        category_list = list(category)      # convert the querryset to a python list

        if not category_list:
            pass

        return JsonResponse(category_list, safe=False)
    except DatabaseError as e:

        print("Database Error:", e)
        return JsonResponse({'error': 'Database error occurred'}, status=500)
    
    except Exception as e:
      
        print("Unexpected Error:", e)

        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

#For finding searched category
def search_category(request):
    if request.method == 'POST':
        # get the searched category
        searched_category = request.POST.get('category-search')

        if searched_category == "":
            pass
        else:
            # filter all the titles and get first title which contains the searched category name
            category = Category.objects.filter(title__icontains=searched_category).first()

            # if the category exists redirect to that sub_category else redirect to same page and show a message
            if category:
                return redirect('home:category:sub_category', slug=category.slug)
            else:
                sweetify.error(request, "Not Found !!")
                return redirect(request.META.get('HTTP_REFERER')) 

    return redirect(request.META.get('HTTP_REFERER'))       

#For the subcategories
def sub_category(request,slug):
    try:
        # get the subcategories using category
        category = get_object_or_404(Category, slug=slug)
        sub_categories = Subcategory.objects.filter(category=category)

        #if there will be empty subcategory queryset then raise an exception
        if not sub_categories:
            raise Subcategory.DoesNotExist
        
        return render(request, 'category/sub_category.html',{'category':category,'sub_categories':sub_categories})
    
    except Subcategory.DoesNotExist:
        #Show an alert box and return category name
        messages.error(request,f"Sorry ! Currently {category.title}s are unavailable")
        return render(request, 'category/sub_category.html', {'category': category, 'sub_categories': []})


#Detail page view of each subcatgory
def detail_view(request, category_slug, sub_category_slug):

    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(Subcategory, slug=sub_category_slug)
    reviews = Review.objects.filter(subcategory=subcategory)
    total_reviews = len(reviews) #total number of reviews for particular category
    

    #Here we calculate the average rating and review of a particular subcategory
    if reviews.exists():
        sum_rating = 0
        count = 0
        for i in reviews:
            sum_rating += i.rating    
            count += 1 
        average_rating = sum_rating / count
        # round to nearest 0.5
        average_rating = round(average_rating * 2) / 2
    else:
        average_rating = None

    #set recently visits category in session
    recent_visits = request.session.get('recent_visits', [])
    recent_visits.insert(0,category_slug) #insert each category_slug at beginning of list
    recent_visits = recent_visits[:4]   #Limit the number of stored recent visits, shows only 4
    request.session['recent_visits'] = recent_visits    

    context = {
        'subcategory': subcategory ,
         'category': category,
         'review': reviews,
         'average_rating':average_rating,
         'total_reviews':total_reviews
    }
    
    return render(request, 'category/detail_view.html', context=context)


@login_required
def submit_review(request, slug):

    url = request.META.get('HTTP_REFERER')   # This URL indicates the previous URL from which the current request originated.
    if request.method == 'POST':
        subcategory = get_object_or_404(Subcategory, slug=slug)

        # Try to get an existing review by the user for the subcategory
        try:
            review = Review.objects.get(user=request.user, subcategory=subcategory)
            form = ReviewForm(request.POST, instance=review)
        except Review.DoesNotExist:
            # If no existing review, create a new one
            form = ReviewForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            data.username = request.user.username
            data.user = request.user
            data.subcategory = subcategory

            # check if the current user has booked this service
            user = request.user
            user_has_booked = BookedSubcategory.objects.filter(
                booking__user=user, subcategory=subcategory
            ).exists()

            #if user booked the particular service then give them  status verified
            if user_has_booked:
                data.status = True
            else:
                data.status = False    

            data.save()
            sweetify.success(request, 'Review submitted successfully')
            return redirect(url)
        else:
            sweetify.error(request, 'Failed to submit review. Form is not valid. Please check the form for errors.')
            return redirect(url)
    else:
        # Retrieve existing review for the user and subcategory
        try:
            review = Review.objects.get(user=request.user, subcategory__slug=slug)
        except Review.DoesNotExist:
            review = None
    
    return redirect(url)


#review displaying view
def show_more_reviews(request):
    try:   
        subcategory_slug = request.GET.get('subcategory_slug') #recive slug from ajax 
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        
        visible = request.GET.get('visible')   #recieve visible from ajax 
        reviews = Review.objects.filter(subcategory=subcategory).order_by('-created_date') #order by created date
        review_size = len(reviews) 
        upper = int(visible) #2 (set the visible value as upper)
        lower = upper - 2 #0 (set lower)
        filtered_reviews = reviews[lower:upper] #slice the two records

        max_size = True if upper >= review_size else False

        
        # render a  template to a string without request(with provided context)
        review_html = render_to_string('category/reviews_partial.html', {'reviews': filtered_reviews})
        
        return JsonResponse({'success':True,'reviews_html':review_html,'max_size':max_size}, safe=False)
    
    except Exception as e:
        return JsonResponse({'success':False,'error_message':str(e)})