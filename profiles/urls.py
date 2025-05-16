from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profile_view, name='profiles'),  # <-- added
    path('profiles/image/', views.change_profile_image, name='change_profile_image'),
    path('profiles/password/', views.change_password, name='change_password'),


]


