from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"


class FoodAnalysis(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='food_analyses'
    )
    image = models.ImageField(upload_to='food_images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    food_name = models.CharField(max_length=255, blank=True, null=True)
    calories = models.FloatField(blank=True, null=True)
    analysis_data = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.food_name or 'Sin nombre'} - {self.user.email}"