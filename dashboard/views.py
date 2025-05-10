from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ProblemStatus, Problem

from django.shortcuts import get_object_or_404, redirect
from problem_list.models import Problem
from django.contrib import messages


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




@login_required
def update_status(request, problem_id):
    if request.method == 'POST':
        problem = get_object_or_404(Problem, id=problem_id)
        new_status = request.POST.get('status')

        status_obj, created = ProblemStatus.objects.get_or_create(
            user=request.user, problem=problem,
            defaults={'status': new_status}
        )
        if not created:
            status_obj.status = new_status
            status_obj.save()

        messages.success(request, f'Status updated to "{new_status.title()}".')
    return redirect(request.META.get('HTTP_REFERER', 'problem_list'))


# =============

