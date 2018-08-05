from django.urls import path, include

from . import views

urlpatterns = [
    path('add/', views.add, name="add anime"),
    path('anime_list/', views.anime_list_redirect, name="anime list redirect"),
    path('<int:anime_id>/', views.anime_page, name="anime page"),
    path('groups/<int:group_id>/', views.usergroup_page, name="group page"),
    path('create_group/', views.create_usergroup, name="create group"),
    path('add_to_group/', views.add_to_usergroup, name="add to group"),
    path('groups/', views.groups, name="groups"),
    path('', views.anime_list, name="anime list"),
]