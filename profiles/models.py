from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    institute = models.CharField(max_length=100, blank=True)
    facebook_link = models.URLField(blank=True)
    discord_username = models.CharField(max_length=100, blank=True)
    vjudge_username = models.CharField(max_length=100, blank=True)
    codeforces_username = models.CharField(max_length=100, blank=True)
    total_unique_solves = models.PositiveIntegerField(default=0)
    codeforces_max_rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
