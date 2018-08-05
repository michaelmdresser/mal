from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils.text import slugify
from anime.forms import SignUpForm, ProfileUpdateForm, AddAnimeForm, CreateGroupForm, AddToGroupForm, RateAnimeForm
from anime.models import UserProfile, Rating, Anime, UserGroup

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

            messages.success(request, "Account created!")
            return redirect('/anime')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            request.user.userprofile.chosen_name = form.cleaned_data.get('chosen_name_updated')
            request.user.userprofile.save()

            messages.success(request, "Name updated!")
            return redirect('/profile')
    else:
        form = ProfileUpdateForm()

    return render(request, 'anime/profile.html', {'user': request.user, 'form': form})

@login_required
def usergroups(request):
    current_usergroup = request.session.get('current_usergroup', None)

    return render(request, 'anime/usergroups.html', {
        'user': request.user,
        'current_usergroup': current_usergroup,
    })

@login_required
def create_usergroup(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            ug = UserGroup()
            ug.name = form.cleaned_data.get('group_name')
            ug.save()
            ug.users.add(request.user)
            ug.save()

            request.session['current_usergroup_id'] = ug.id
            messages.success(request, "Created group \"%s\"" % ug.name)
            return redirect('/anime/groups')
    else:
        form = CreateGroupForm()
    
    return render(request, 'anime/create_group.html', {'form': form, 'message': message})

@login_required
def add_to_usergroup(request):
    if not request.session.get('current_usergroup_id'):
        messages.info(request, "No selected group")
        return redirect('/anime')

    ug_id = request.session.get('current_usergroup_id')
    ug = get_object_or_404(UserGroup, pk=ug_id)

    if request.method == 'POST':
        form = AddToGroupForm(request.POST)
        if form.is_valid():
            ug.users.add(User.objects.all().filter(username=form.cleaned_data.get('username')))    
            ug.save()
            return redirect("/groups")
    else:
        form = AddToGroupForm()
    
    return render(request, 'anime/add_to_group.html', {'form': form})

@login_required
def usergroup_page(request, group_id):
    usergroup = get_object_or_404(UserGroup, pk=group_id)
    user = request.user

    try:
        usergroup.users.get(pk=user.id)
    except User.DoesNotExist:
        messages.info(request, "You do not belong to this group")
        return redirect('/anime')
    
    if request.POST.get('activate_button'):
        request.session['current_usergroup_id'] = group_id
        messages.success(request, "Set as current group")

    return render(request, 'anime/group_page.html', {
        'usergroup': usergroup,
        'usergroup_users': usergroup.users.all()
    })

@login_required
def groups(request):
    ug_id = request.session.get('current_usergroup_id', None)
    try:
        current_usergroup = UserGroup.objects.get(pk=ug_id)
    except UserGroup.DoesNotExist:
        current_usergroup = None

    user = request.user
    usergroup_set = user.usergroup_set.all()

    return render(request, 'anime/groups.html', {
        'current_usergroup': current_usergroup,
        'usergroup_set': usergroup_set,
        'user': user
    })


@login_required
def anime_list(request):
    anime_list = Anime.objects.all()

    ug_id = request.session.get('current_usergroup_id', None)
    try:
        current_usergroup = UserGroup.objects.get(pk=ug_id)
    except UserGroup.DoesNotExist:
        current_usergroup = None

    if current_usergroup:
        user_list = current_usergroup.users.exclude(pk=request.user.id)
    else:
        user_list = None

    user = request.user

    return render(request, 'anime/anime_table.html', {
        'anime_list': anime_list,
        'user_list': user_list,
        'user': user,
        'current_usergroup': current_usergroup,
    })

def anime_list_redirect(request):
    return redirect('/anime')

@login_required
def anime_page(request, anime_id):
    if request.method == 'POST':
        form = RateAnimeForm(request.POST)
        if form.is_valid():
            existing_r = Rating.objects.filter(user__id=request.user.id, anime__id=anime_id)
            rating = form.cleaned_data.get('rating')
            if len(existing_r) == 0:
                r = Rating()
                r.user = request.user
                r.value = rating
                r.anime = get_object_or_404(Anime, pk=anime_id)
                r.save()
            else:
                existing_r[0].value = rating
                existing_r[0].save()
        
        return redirect('/anime/%s' % anime_id)
    else:
        form = RateAnimeForm()

    anime = get_object_or_404(Anime, pk=anime_id)
    user = request.user
    rating = Rating.objects.filter(anime__id=anime.id, user__id=user.id)
    if len(rating) == 0:
        rating = None
    else:
        rating = rating[0]

    return render(request, 'anime/anime_page.html', {
        'anime': anime,
        'rating': rating,
        'form': form
    })

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

            if len(Anime.objects.filter(clean_full_name=a.clean_full_name)) > 0:
                return render(request, 'anime/add.html', {'message': "What you tried to add seems to already exist"})

            a.save()
            request.session['message'] = "Added anime %s/%s" % (a.name, a.name_secondary)
            return redirect('/anime')
    else:
        form = AddAnimeForm()
    
    return render(request, 'anime/add.html', {
        'form': form
    })