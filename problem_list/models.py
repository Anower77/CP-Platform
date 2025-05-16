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

    bookmarked_by = models.ManyToManyField(
        User,
        through='dashboard.Bookmark',
        related_name='bookmarked_problems',
        blank=True
    )

    title = models.CharField(max_length=255, unique=True)
    editorial_link = models.URLField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    code = models.TextField()
    rating = models.IntegerField(default=800)
    ac_rate = models.BooleanField(default=False)
    source = models.CharField(max_length=255, blank=True, null=True)
    starred = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    is_external = models.BooleanField(default=False)
    external_url = models.URLField(blank=True, null=True) 
    
    def __str__(self):
        return self.title


# status per use
class ProblemStatus(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('reading', 'Reading'),
        ('practicing', 'Practicing'),
        ('complete', 'Complete'),
        ('skipped', 'Skipped'),
        ('ignored', 'Ignored'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_list_problem_statuses')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem_list_problem_statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    bookmarked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'problem']

