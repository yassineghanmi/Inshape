# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.nutrition_list, name='nutrition_list'),
    path('nutrition/new', views.nutrition_create, name='nutrition_create'),
    path('nutrition/<int:pk>/edit', views.nutrition_update, name='nutrition_update'),
     path('nutrition/<int:pk>/delete', views.nutrition_delete, name='nutrition_delete'),
    path('add_by_barcode/', views.add_by_barcode, name='add_by_barcode'),
    path('add_nutrition/', views.add_nutrition, name='add_nutrition'),
   path('nutrition/<int:pk>/', views.nutrition_detail, name='nutrition_detail'),
]
