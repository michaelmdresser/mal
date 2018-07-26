from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import django_tables2 as tables
from django_tables2.utils import A

import os

from .models import Media, Rating, User

# Create your views here.
def index(request):
    
    anime_list = Media.objects.all()
    template = loader.get_template('anime/index.html')
    context = {
        'anime_list': anime_list,
    }
    return HttpResponse(template.render(context, request))

class SimpleTable(tables.Table):
    class Meta:
        model = Media
        #model = Rating

class AnimeTable(tables.Table):
    name = tables.Column()
    name_secondary = tables.Column()
    class Meta:
        model = Media

def simple_list(request):
    media_queryset = Media.objects.all()
    ratings_queryset = Rating.objects.all()
    table = SimpleTable(data=media_queryset)
    #table = AnimeTable(queryset)
    return render(request, 'simple_list.html', {'table': table})

def anime_list(request):
    template = loader.get_template('anime/anime_table.html')
    context = {
        'anime_list': Media.objects.all(),
        'user_list': User.objects.all(),
    }

    return HttpResponse(template.render(context, request))