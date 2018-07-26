from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('simple_list/', views.simple_list, name="simple list"),
    path('anime_list/', views.anime_list, name="anime list"),
]