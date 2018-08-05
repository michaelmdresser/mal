from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Anime(models.Model):
    name = models.CharField(blank=False, max_length=200)
    name_secondary = models.CharField(max_length=200, default="")
    clean_full_name = models.CharField(blank=False, max_length=450, unique=True)
    
    def __str__(self):
        return self.name + "/" + self.name_secondary


class Rating(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return self.user.username + "@" + self.anime.name + ": " + str(self.value)
    
    class Meta:
        unique_together = (("anime", "user"))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    chosen_name = models.CharField(blank=False, max_length=255)

    class Meta:
        ordering = ['user']
        verbose_name = 'user'
        verbose_name_plural = 'users'

class UserGroup(models.Model):
    name = models.CharField(blank=False, max_length=255)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)