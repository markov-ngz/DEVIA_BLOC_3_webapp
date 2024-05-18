from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Translation(models.Model):

    text = models.CharField(max_length=256)
    translation = models.CharField(max_length=256)
    # created_by = models.ForeignKey(User, related_name='translations')
    created_at = models.DateTimeField(auto_now_add=True)
    