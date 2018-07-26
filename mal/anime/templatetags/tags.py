from django.template import Library
from anime.models import Rating
from django.db.models import Avg

register = Library()

@register.simple_tag
def get_user_rating_for_anime(user, anime):
    r = Rating.objects.filter(user__id=user.id, media__id=anime.id).values()
    if len(r) == 0:
        return ""
    return Rating.objects.filter(user__id=user.id, media__id=anime.id).values()[0]['value']

@register.simple_tag
def get_average_for_anime(anime):
    avg = Rating.objects.filter(media__id=anime.id).aggregate(Avg('value'))['value__avg']
    return avg

@register.simple_tag
def get_median_for_anime(anime):
    ratings = Rating.objects.filter(media__id=anime.id).all()

    count = ratings.count()
    values = ratings.values_list('value', flat=True).order_by('value')
    
    median = None
    if count % 2 == 1:
        median = values[int(round(count/2))]
    else:
        median = sum(values[count/2-1:count/2+1])/2

    return median