from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Anime(models.Model):
    name = models.CharField(max_length=200)
    name_secondary = models.CharField(max_length=200, default="")
    
    def __str__(self):
        return self.name + "/" + self.name_secondary

class Rating(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return self.user.name + "@" + self.anime.name + ": " + str(self.value)