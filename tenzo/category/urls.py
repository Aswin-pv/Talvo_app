from django.urls import path,include
from . import views

app_name = 'category'

urlpatterns = [
    path('', views.category, name='category'),
    path('<slug:slug>/',views.sub_category,name='sub_category'),
     path('<slug:category_slug>/<slug:sub_category_slug>/', views.employee_list, name='employee_list'),
]
