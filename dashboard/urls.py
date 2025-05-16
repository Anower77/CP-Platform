from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_status/<int:problem_id>/', views.update_status, name='update_status'),
    path('toggle-bookmark/<int:problem_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    # path('bookmark/<int:problem_id>/', views.toggle_bookmark, name='toggle_bookmark'),

]
