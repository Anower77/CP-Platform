from django.urls import path
from . import views

urlpatterns = [
    path('contest/', views.contest, name='contest'),

]