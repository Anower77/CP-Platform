from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('update_status/<int:problem_id>/', views.update_status, name='update_status'),

]
