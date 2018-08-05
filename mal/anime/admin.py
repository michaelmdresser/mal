from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Anime, Rating, UserProfile, UserGroup


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    #filter_horizontal = ['filter fields']
    verbose_name_plural = 'user profiles'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    #list_display = ('username', 'email', 'chosen_name', 'first_name', 'last_name', 'is_staff')
    #list_filter = ('is_staff', 'is_superuser', 'is_active')


admin.site.register(Anime)
admin.site.register(Rating)
admin.site.register(UserGroup)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)