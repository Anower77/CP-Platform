from django.urls import path
from . import views

urlpatterns = [
    path('problem_list/', views.problem_list, name='problem_list'),
    path('problem/<int:pk>/', views.problem_detail, name='problem_detail'),  # <-- added
    path('problem/<int:problem_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('problem/<int:problem_id>/update_status/', views.update_status, name='update_status'),
    path('get-code/<int:problem_id>/', views.get_code, name='get_code'),
    path('get-video/<int:problem_id>/', views.get_video, name='get_video'),

    # path('get-code/<int:pk>/', views.get_code, name='get_code'),


]