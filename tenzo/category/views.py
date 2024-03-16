from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Subcategory,Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm
from django.http import JsonResponse
from django.core.paginator import Paginator


@login_required
def category(request):
    # to get all the categories
    categories = Category.objects.all()

    # paginator for displaying multiple pages
    paginator = Paginator(categories,2)
    page_number = request.GET.get('page')
    categoryfinal = paginator.get_page(page_number)
    total_pages = categoryfinal.paginator.num_pages 

    context = {
        'categoryfinal' : categoryfinal,
        'last_page': total_pages,
        'totalpagelist': [n+1 for n in range(total_pages)],
    }

    return render(request, "category/category.html", context=context)


def search_list(request):
    # retrieves a list of values for the title field
    category = Category.objects.filter().values_list('title', flat=True) #gives a flat list rather than the tuples
    
    # convert the querryset to a python list
    category_list = list(category)

    return JsonResponse(category_list,safe=False)

def search_category(request):

    if request.method == 'POST':
        # get the searched category
        searched_category = request.POST.get('category-search')

        if searched_category == "":
            return redirect(request.Meta.get('HTTP_REFERER')) 
        else:
            # filter all the titles and get first title which contains the searched category name
            category = Category.objects.filter(title__icontains=searched_category).first()

            # if the category exists redirect to that category else redirect to same page
            if category:
                return redirect('home:category:sub_category', slug=category.slug)
            else:
                messages.info(request, 'No categories Matched')
                return redirect(request.Meta.get('HTTP_REFERER')) 

    return redirect(request.Meta.get('HTTP_REFERER'))       


def sub_category(request,slug):
    category = get_object_or_404(Category, slug=slug)
    sub_categories = Subcategory.objects.filter(category=category)
    return render(request, 'category/sub_category.html',{'category':category,'sub_categories':sub_categories})


def detail_view(request, category_slug, sub_category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(Subcategory, slug=sub_category_slug)
    reviews = Review.objects.filter(subcategory=subcategory)
    total_reviews = len(reviews)


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

    context = {
        'subcategory': subcategory ,
         'category': category,
         'reviews':reviews,
         'average_rating':average_rating,
         'total_reviews':total_reviews
    }
    
    return render(request, 'category/detail_view.html', context=context)


@login_required
def submit_review(request, slug):
    url = request.META.get('HTTP_REFERER')
    print(slug)
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
            data.user = request.user
            data.subcategory = subcategory
            data.save()
            messages.success(request, 'Review submitted successfully')
            return redirect(url)
        else:
            messages.error(request, 'Failed to submit review. Form is not valid. Please check the form for errors.')
            return redirect(url)
    else:
        # Retrieve existing review for the user and subcategory
        try:
            review = Review.objects.get(user=request.user, subcategory__slug=slug)
        except Review.DoesNotExist:
            review = None
    
    return redirect(url)


def load_more_reviews(request):
    page = request.GET.get('page', 1)
    per_page = 1  # Adjust the number of reviews per page as needed
    start_index = (page - 1) * per_page
    end_index = page * per_page

    reviews = Review.objects.all()[start_index:end_index]

    review_html = ''  # Placeholder for the HTML content of the reviews
    for review in reviews:
        # Generate HTML content for each review (customize as needed)
        review_html += f"""
            <div class="d-flex border-bottom pb-5 mb-5">
                <div class="ms-5">
                    <h6 class="mb-1">{review.user.username}</h6>
                    <p class="small">
                        <span class="text-muted">{review.created_date}</span>
                        <span class="text-primary ms-3 fw-bold">Verified Purchase</span>
                    </p>
                    <div class="rating-display mb-2">
                        {review.rating}
                    </div>
                    <p>
                        {review.comment}
                    </p>
                </div>
            </div>
        """

    return JsonResponse({'review_html': review_html})