from django.urls import path, include

from . import views

urlpatterns = [
    path('add/', views.add, name="add anime"),
    path('anime_list/', views.anime_list_redirect, name="anime list redirect"),
    path('', views.anime_list, name="anime list"),
]