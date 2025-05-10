from django.db import models
from django.contrib.auth.models import User
from problem_list.models import Problem

class ProblemStatus(models.Model):
    STATUS_CHOICES = Problem.STATUS_CHOICES

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    timer = models.IntegerField(default=0)
    bookmarked = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'problem')  # ensures 1 entry per user per problem

    def __str__(self):
        return f'{self.user.username} - {self.problem.title} ({self.status})'
