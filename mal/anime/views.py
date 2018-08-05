from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, authenticate
from django.utils.text import slugify
from anime.forms import SignUpForm, ProfileUpdateForm, AddAnimeForm
from anime.models import UserProfile, Rating, Anime

import os

from .models import Anime, Rating

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            userprofile = UserProfile(chosen_name=form.cleaned_data.get('chosen_name'), user=user)
            userprofile.save()

            content_type = ContentType.objects.get_for_model(Rating)
            permission = Permission.objects.get(content_type=content_type, codename='add_rating')
            user.user_permissions.add(permission)

            content_type = ContentType.objects.get_for_model(Anime)
            permission = Permission.objects.get(content_type=content_type, codename='add_anime')
            user.user_permissions.add(permission)

            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/anime')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    message = request.session.pop('message', None)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            request.user.userprofile.chosen_name = form.cleaned_data.get('chosen_name_updated')
            request.user.userprofile.save()
            return redirect('/profile')
    else:
        form = ProfileUpdateForm()

    return render(request, 'anime/profile.html', {'user': request.user, 'message': message, 'form': form})

@login_required
def anime_list(request):
    anime_list = Anime.objects.all()
    user_list = User.objects.all().exclude(pk=request.user.id)
    user = request.user
    # if len(Anime.objects.all()) > 0:
    #     anime_list = Anime.objects.all()
    message = request.session.pop('message', None)

    return render(request, 'anime/anime_table.html', {'anime_list': anime_list, 'user_list': user_list, 'user': user, 'message': message})

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
    
    if request.method == 'POST':
        form = AddAnimeForm(request.POST)
        if form.is_valid():
            a = Anime()
            a.name = form.cleaned_data.get('english_name')
            a.name_secondary = form.cleaned_data.get('japanese_name')
            a.clean_full_name = slugify(a.name.lower() + '/' + a.name_secondary.lower())
            a.save()
            request.session['message'] = "Added anime %s/%s" % (a.name, a.name_secondary)
            return redirect('/anime')
    else:
        form = AddAnimeForm()
    
    return render(request, 'anime/add.html', {'form': form})

    # if len(request.POST) == 0:
    #     return render(request, 'anime/add.html')
    
    # if len(request.POST['english_name']) == 0 or len(request.POST['japanese_name']) == 0:
    #     return render(request, 'anime/add.html', {'message': "Please fill in both fields"})
    
    # if len(Anime.objects.filter(name__iexact=request.POST['english_name']) | Anime.objects.filter(name_secondary__iexact=request.POST['japanese_name'])) > 0:
    #     return render(request, 'anime/add.html', {'message': "What you tried to add seems to already exist"})
    
    # a = Anime()
    # a.name = request.POST['english_name']
    # a.name_secondary = request.POST['japanese_name']
    # a.clean_full_name = slugify(request.POST['english_name'].lower() + '/' + request.POST['japanese_name'].lower())
    # a.save()

    # request.session['message'] = "Added anime %s/%s" % (a.name, a.name_secondary)
    # return redirect('/anime')

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