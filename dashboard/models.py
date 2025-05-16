from django.db import models
from django.contrib.auth.models import User
from problem_list.models import Problem


class ProblemStatus(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('reading', 'Reading'),
        ('practicing', 'Practicing'),
        ('complete', 'Complete'),
        ('skipped', 'Skipped'),
        ('ignored', 'Ignored'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_problem_statuses')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='dashboard_problem_statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    bookmarked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'problem']

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.status}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_bookmarks')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='dashboard_problem_bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'problem')

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
