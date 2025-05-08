from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem

choices = Problem.STATUS_CHOICES


# Create your views here.
@login_required(login_url='login')
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'Problem List/problem_list.html', {'problems': problems})


@login_required(login_url='login')
def problem_detail(request, pk):
    problem = Problem.objects.get(pk=pk)
    return render(request, 'Problem List/problem_detail.html', {'problem': problem})


@login_required(login_url='login')
def toggle_bookmark(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    if request.user in problem.bookmarked_by.all():
        problem.bookmarked_by.remove(request.user)  # Unbookmark
    else:
        problem.bookmarked_by.add(request.user)  # Bookmark
    return redirect('problem_list')  # Redirect back to problem list (you can change it)


@login_required(login_url='login')
def update_status(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Problem.STATUS_CHOICES).keys():
            problem.status = status
            problem.save()
    return redirect('problem_list')  # replace with your actual list view name
