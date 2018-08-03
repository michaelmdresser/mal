from django.urls import path, include

from . import views

urlpatterns = [
    path('add/', views.add, name="add anime"),
    path('anime_list/', views.anime_list_redirect, name="anime list redirect"),
    path('<int:anime_id>/', views.anime_page, name="anime page"),
    path('rate/', views.rate, name="rate page"),
    path('', views.anime_list, name="anime list"),
]