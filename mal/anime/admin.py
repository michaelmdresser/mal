from django.contrib import admin

from .models import Media, Rating, User

admin.site.register(Media)
admin.site.register(Rating)
admin.site.register(User)