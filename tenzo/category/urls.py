from django.urls import path,include
from . import views

app_name = 'category'

urlpatterns = [
    path('', views.category, name='category'),
    path('<int:pk>/',views.sub_category,name='sub_category')
]
