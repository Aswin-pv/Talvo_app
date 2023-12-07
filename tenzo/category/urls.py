from django.urls import path,include
from . import views

app_name = 'category'

urlpatterns = [
    path('', views.category, name='category'),
    path('<slug:slug>/',views.sub_category,name='sub_category'),
    path('submit_review/<slug:slug>/',views.submit_review,name='submit_review'),
    path('<slug:category_slug>/<slug:sub_category_slug>/', views.detail_view, name='detail_view'),
]
