from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem
from django.http import JsonResponse
import re

choices = Problem.STATUS_CHOICES


# Create your views here.
@login_required(login_url='login')
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'Problem List/problem_list.html', {'problems': problems})


@login_required(login_url='login')
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    if problem.is_external and problem.external_url:
        return redirect(problem.external_url)

    return render(request, 'Problem List/problem_detail.html', {'problem': problem})


@login_required(login_url='login')
def toggle_bookmark(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    if request.user in problem.bookmarked_by.all():
        problem.bookmarked_by.remove(request.user)  
    else:
        problem.bookmarked_by.add(request.user)  
    return redirect('problem_list')  


@login_required(login_url='login')
def update_status(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Problem.STATUS_CHOICES).keys():
            problem.status = status
            problem.save()
    return redirect('problem_list')  

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
