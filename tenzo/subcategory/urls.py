from django.urls import path,include
from . import views

app_name = 'subcategory'

urlpatterns = [
    path('', views.sub_category, name='sub_category'),
]
