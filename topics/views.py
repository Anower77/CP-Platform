from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Topic, Visualization

# Create your views here.
def topics(request):
    return render(request, 'topics/topics.html')