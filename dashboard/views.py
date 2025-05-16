from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ProblemStatus, Problem, Bookmark
from django.shortcuts import get_object_or_404, redirect
from problem_list.models import Problem
from django.contrib import messages

@login_required
def dashboard(request):
    user = request.user

    # Get problem statuses
    user_statuses = ProblemStatus.objects.filter(user=user)

    # Count status categories
    status_data = {
        'bookmarked': Bookmark.objects.filter(user=user).count(),
        'reading': user_statuses.filter(status='reading').count(),
        'practicing': user_statuses.filter(status='practicing').count(),
        'complete': user_statuses.filter(status='complete').count(),
        'skipped': user_statuses.filter(status='skipped').count(),
        'ignored': user_statuses.filter(status='ignored').count(),
    }

    # Get only bookmarked problems
    bookmarked_problems = Problem.objects.filter(
        dashboard_problem_bookmarks__user=user
    ).distinct().order_by('-dashboard_problem_bookmarks__created_at')

    # Get status and bookmark info for each problem
    for problem in bookmarked_problems:
        # Get user's status for this problem
        problem.user_status = user_statuses.filter(problem=problem).first()
        # Set is_bookmarked to True since these are all bookmarked problems
        problem.is_bookmarked = True

    context = {
        'status_data': status_data,
        'dashboard_problems': bookmarked_problems,
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def update_status(request, problem_id):
    if request.method == 'POST':
        problem = get_object_or_404(Problem, id=problem_id)
        new_status = request.POST.get('status')

        # Update status in dashboard app
        status_obj, created = ProblemStatus.objects.get_or_create(
            user=request.user, 
            problem=problem,
            defaults={'status': new_status}
        )
        if not created:
            status_obj.status = new_status
            status_obj.save()

        # Update status in problem_list app
        from problem_list.models import ProblemStatus as ProblemListStatus
        problem_list_status, created = ProblemListStatus.objects.get_or_create(
            user=request.user,
            problem=problem,
            defaults={'status': new_status}
        )
        if not created:
            problem_list_status.status = new_status
            problem_list_status.save()

        messages.success(request, f'Status updated to "{new_status.title()}".')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def toggle_bookmark(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    user = request.user

    bookmark, created = Bookmark.objects.get_or_create(user=user, problem=problem)

    if not created:
        bookmark.delete()  # unbookmark if already exists
        messages.success(request, f'Problem "{problem.title}" removed from bookmarks.')
    else:
        messages.success(request, f'Problem "{problem.title}" added to bookmarks.')

    # Update ProblemStatus bookmarked field
    problem_status, _ = ProblemStatus.objects.get_or_create(
        user=user,
        problem=problem,
        defaults={'status': 'not_started'}
    )
    problem_status.bookmarked = created
    problem_status.save()

    # Update ProblemListStatus bookmarked field
    from problem_list.models import ProblemStatus as ProblemListStatus
    problem_list_status, _ = ProblemListStatus.objects.get_or_create(
        user=user,
        problem=problem,
        defaults={'status': 'not_started'}
    )
    problem_list_status.bookmarked = created
    problem_list_status.save()

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
