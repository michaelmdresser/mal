from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

import os

from .models import Anime, Rating

@login_required
def anime_list(request):
    anime_list = Anime.objects.all()
    user_list = User.objects.all()
    # if len(Anime.objects.all()) > 0:
    #     anime_list = Anime.objects.all()
    message = request.session.pop('message', None)

    return render(request, 'anime/anime_table.html', {'anime_list': anime_list, 'user_list': user_list, 'message': message})

def anime_list_redirect(request):
    return redirect('/anime')

@login_required
def add(request):
    if not request.user.has_perm('anime.add_anime'):
        request.session['message'] = "you do not have permissions to add anime"
        return redirect('/anime')

    if len(request.POST) == 0:
        return render(request, 'anime/add.html')
    
    if len(request.POST['english_name']) == 0 or len(request.POST['japanese_name']) == 0:
        return render(request, 'anime/add.html', {'message': "Please fill in both fields"})
    
    if len(Anime.objects.filter(name__iexact=request.POST['english_name']) | Anime.objects.filter(name_secondary__iexact=request.POST['japanese_name'])) > 0:
        return render(request, 'anime/add.html', {'message': "What you tried to add seems to already exist"})
    
    a = Anime()
    a.name = request.POST['english_name']
    a.name_secondary = request.POST['japanese_name']
    a.save()

    request.session['message'] = "Added anime %s/%s" % (a.name, a.name_secondary)
    return redirect('/anime')