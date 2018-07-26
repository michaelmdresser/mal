from django.db import models

# Create your models here.
class Media(models.Model):
    name = models.CharField(max_length=200)
    name_secondary = models.CharField(max_length=200, default="")
    
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Rating(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return self.media.name + ": " + str(self.value)