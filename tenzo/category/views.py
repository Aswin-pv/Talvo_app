from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Subcategory,Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm



def category(request):
    categories = Category.objects.all()
    return render(request, "category/category.html", { 'categories' : categories })


def sub_category(request,slug):
    category = get_object_or_404(Category, slug=slug)
    sub_categories = Subcategory.objects.filter(category=category)
    return render(request, 'category/sub_category.html',{'sub_categories':sub_categories})


def detail_view(request, category_slug, sub_category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(Subcategory, slug=sub_category_slug)
    
    return render(request, 'category/detail_view.html',{'subcategory': subcategory ,'category': category})


@login_required
def submit_review(request, slug):
    url = request.META.get('HTTP_REFERER')

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
            # Print form errors for debugging
            print(form.errors)
            return redirect(url)

    messages.error(request, 'Failed to submit review. Please try again.')
    return redirect(url)
