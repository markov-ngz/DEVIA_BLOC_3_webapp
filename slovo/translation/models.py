from django.db import models

# Create your models here.
class Translation(models):
    text = models.CharField(max_length=512)
    translation = models.CharField(max_length=512)
    