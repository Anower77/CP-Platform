from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home_feed.urls")),
    path('problem_list/', include("problem_list.urls")),
    path('authentication/', include("authentication.urls")),
    path('contest/', include("contest.urls")),
    path('profiles/', include("profiles.urls")),
    path('dashboard/', include('dashboard.urls')),
    path('topics/', include('topics.urls')),

    # About page URL
    path('about/',views.about, name='about'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)