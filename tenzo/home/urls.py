from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'home'

urlpatterns = [
    path('home/', views.home, name ='home'),
    path('login/',LoginView.as_view(success_url = '/home/'),name='login'),
]
