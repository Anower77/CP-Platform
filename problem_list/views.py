from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem, ProblemStatus
from django.http import JsonResponse
from problem_list.models import Problem
from django.db.models import Count, Q
from dashboard.models import Bookmark
import re

choices = Problem.STATUS_CHOICES


# Create your views here.
@login_required(login_url='login')
def problem_list(request):
    query = request.GET.get("q")

    problems = Problem.objects.all()

    if query:
        problems = problems.filter(
            Q(title__icontains=query) |
            Q(problem_list_problem_statuses__status__icontains=query) |
            Q(source__icontains=query) |
            Q(rating__icontains=query)
        )

    # Annotate the complete count (AC count)
    problems = problems.annotate(
        complete_count=Count(
            'problem_list_problem_statuses',
            filter=Q(problem_list_problem_statuses__status='complete')
        )
    )

    # Attach each problem's status for this user
    user_status_map = {
        ps.problem_id: ps.status
        for ps in ProblemStatus.objects.filter(user=request.user)
    }

    for p in problems:
        p.user_status = user_status_map.get(p.id, 'not_started')

    context = {
        'problems': problems,
        'user_status_choices': ProblemStatus.STATUS_CHOICES,
    }

    return render(request, 'Problem List/problem_list.html', context)


@login_required(login_url='login')
def update_status(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    user = request.user

    if request.method == 'POST':
        new_status = request.POST.get('status')

        # Update status in problem_list app
        problem_status, created = ProblemStatus.objects.get_or_create(
            user=user,
            problem=problem,
            defaults={'status': new_status}
        )
        if not created:
            problem_status.status = new_status
            problem_status.save()

        # Update status in dashboard app
        from dashboard.models import ProblemStatus as DashboardProblemStatus
        dashboard_status, created = DashboardProblemStatus.objects.get_or_create(
            user=user,
            problem=problem,
            defaults={'status': new_status}
        )
        if not created:
            dashboard_status.status = new_status
            dashboard_status.save()

        # Update complete count if needed
        if new_status == 'complete':
            complete_count = ProblemStatus.objects.filter(
                problem=problem,
                status='complete'
            ).count()
            problem.complete_count = complete_count
            problem.save()

    return redirect(request.META.get('HTTP_REFERER', 'problem_list'))



@login_required(login_url='login')
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if problem.is_external and problem.external_url:
        return redirect(problem.external_url)
    return render(request, 'Problem List/problem_detail.html', {'problem': problem})




@login_required(login_url='login')
def toggle_bookmark(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    user = request.user
    
    bookmark, created = Bookmark.objects.get_or_create(user=user, problem=problem)
    
    if not created:
        bookmark.delete()  # unbookmark if already exists
        
    # Update the ProblemStatus bookmarked field
    problem_status, _ = ProblemStatus.objects.get_or_create(
        user=user,
        problem=problem,
        defaults={'status': 'not_started'}
    )
    problem_status.bookmarked = created
    problem_status.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'problem_list'))


# @login_required(login_url='login')
# def update_status(request, problem_id):
#     problem = get_object_or_404(Problem, pk=problem_id, user=request.user)
#     if request.method == 'POST':
#         status = request.POST.get('status')
#         if status in dict(Problem.STATUS_CHOICES).keys():
#             problem.status = status
#             problem.save()
#     return redirect('problem_list')  

# def update_status(request, problem_id):
#     problem = get_object_or_404(Problem, id=problem_id, user=request.user)

#     if request.method == 'POST':
#         new_status = request.POST.get('status')
#         problem.status = new_status

#         # Mark is_ac as True if "Complete", else False
#         problem.is_ac = True if new_status == 'complete' else False
#         problem.save()

#     return redirect('your_problem_list_url_name')


# ==============================
# @login_required
# def update_status(request, problem_id):
#     if request.method == "POST":
#         problem = get_object_or_404(Problem, id=problem_id)
#         new_status = request.POST.get('status', 'not_started')

#         # Save the new status (per user if applicable)
#         problem.status = new_status
#         problem.save()

#     return redirect(request.META.get('HTTP_REFERER', '/'))




@login_required(login_url='login')
def get_code(request, problem_id):
    try:
        problem = Problem.objects.get(pk=problem_id)
        return JsonResponse({'code': problem.code})
    except Problem.DoesNotExist:
        return JsonResponse({'error': 'Problem not found'}, status=404)


@login_required(login_url='login')
def extract_youtube_id(url):
    regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(regex, url)
    return match.group(1) if match else None


@login_required(login_url='login')
def get_video(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    return JsonResponse({'video_url': problem.video_link})




# @login_required(login_url='login')
# def update_status(request, problem_id):
#     # Get the problem object
#     problem = get_object_or_404(Problem, id=problem_id)

#     if request.method == 'POST':
#         # Get the selected status from the form
#         status = request.POST.get('status')

#         # Get the current logged-in user
#         user = request.user

#         # Check if there is an existing ProblemStatus for this user and problem
#         problem_status, created = ProblemStatus.objects.get_or_create(user=user, problem=problem)

#         # Update the status
#         problem_status.status = status
#         problem_status.save()

#     # Redirect back to the problem page or wherever you want after the update
#     return redirect('problem_detail', problem_id=problem.id)



# @login_required(login_url='login')
# def update_status(request, problem_id):
#     problem = get_object_or_404(Problem, id=problem_id)
#     user = request.user

#     if request.method == 'POST':
#         new_status = request.POST.get('status')

#         # Get or create ProblemStatus for this user and problem
#         problem_status, created = ProblemStatus.objects.get_or_create(
#             user=user,
#             problem=problem
#         )

#         # Update status
#         problem_status.status = new_status
#         problem_status.save()

#     return redirect('problem_list')  # Or 'problem_detail', as needed
