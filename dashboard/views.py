from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ProblemStatus

@login_required
def dashboard_view(request):
    status_qs = ProblemStatus.objects.filter(user=request.user)

    status_data = {
        'bookmarked': status_qs.filter(bookmarked=True).count(),
        'reading': status_qs.filter(status='reading').count(),
        'practicing': status_qs.filter(status='practicing').count(),
        'complete': status_qs.filter(status='complete').count(),
        'skipped': status_qs.filter(status='skipped').count(),
        'ignored': status_qs.filter(status='ignored').count(),
    }

    return render(request, 'dashboard/dashboard.html', {'status_data': status_data})
