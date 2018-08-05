from django.urls import path, include

from . import views

urlpatterns = [
    path('add/', views.add, name="add anime"),
    path('anime_list/', views.anime_list_redirect, name="anime list redirect"),
    path('<int:anime_id>/', views.anime_page, name="anime page"),
    path('<int:group_id', views.group_page, name="group page"),
    path('create_group/', views.create_group, name="create group"),
    path('add_to_group/', views.add_to_group, name="add to group"),
    path('groups/', views.groups, name="groups"),
    path('rate/', views.rate, name="rate page"),
    path('', views.anime_list, name="anime list"),
]