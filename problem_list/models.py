from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('reading', 'Reading'),
        ('practicing', 'Practicing'),
        ('complete', 'Complete'),
        ('skipped', 'Skipped'),
        ('ignored', 'Ignored'),
    ]

    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_problems', blank=True)
    title = models.CharField(max_length=255)
    editorial_link = models.URLField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    code_link = models.URLField(blank=True, null=True)
    timer = models.IntegerField(default=0)
    ac_rate = models.FloatField(default=0.0)
    source = models.CharField(max_length=255, blank=True, null=True)
    starred = models.BooleanField(default=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return self.title
