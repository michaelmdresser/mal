from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.utils.text import slugify

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
def anime_page(request, anime_id):
    anime = get_object_or_404(Anime, pk=anime_id)
    user = request.user
    rating = Rating.objects.filter(anime__id=anime.id, user__id=user.id)
    if len(rating) == 0:
        rating = None
    else:
        rating = rating[0]

    message = request.session.pop('message', None)
    return render(request, 'anime/anime_page.html', {'message': message, 'anime': anime, 'rating': rating})

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
    a.clean_full_name = slugify(request.POST['english_name'].lower() + '/' + request.POST['japanese_name'].lower())
    a.save()

    request.session['message'] = "Added anime %s/%s" % (a.name, a.name_secondary)
    return redirect('/anime')

@login_required
def rate(request):
    if not request.user.has_perm('anime.add_rating'):
        request.session['message'] = "you do not have permissions to rate anime"
        return redirect('/anime')
    
    if len(request.POST) == 0:
        return redirect('/anime')

    if 'anime_id' not in request.POST:
        request.session['message'] = "no anime_id set?"
        return redirect('/anime/%s' % request.POST['anime_id'])
    
    if 'rating' not in request.POST:
        request.session['message'] = "You must enter a rating"
        return redirect('/anime/%s' % request.POST['anime_id'])
    
    rating = request.POST['rating']
    existing_r = Rating.objects.filter(user__id=request.user.id, anime__id=request.POST['anime_id'])
    if len(existing_r) == 0:
        r = Rating()
        r.user = request.user
        r.value = rating
        r.anime = get_object_or_404(Anime, pk=request.POST['anime_id'])
        r.save()
    else:
        existing_r[0].value = rating
        existing_r[0].save()

    request.session['message'] = "Rated %s" % rating
    return redirect('/anime/%s' % request.POST['anime_id'])