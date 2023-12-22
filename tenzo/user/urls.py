from django.urls import path
from . import views


urlpatterns = [
   path('',views.profile,name='profile'),
   path('update/<pk>',views.update_profile, name='update'),
   path('address/',views.address_list, name='address_list'),
   path('address/add',views.add_address, name='add_address'),
   path('address/edit/<int:pk>/',views.edit_address, name='edit_address'),
   path('address/delete/',views.delete_address, name='delete_address'),

]
