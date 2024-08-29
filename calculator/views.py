from django.shortcuts import render
from .models import Project, Transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .forms import ActorForm, TransactionForm, UseCaseForm


def index(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'projects': projects})


def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            project = Project.objects.create(name=name, description=description)
            return redirect(reverse('project_detail', args=[project.id]))
    return redirect('index')


def project_detail(request, project_id):
    project = Project.objects.get(pk=project_id)
    actors = project.actors.all()
    use_cases = project.use_cases.all()
    transactions = Transaction.objects.filter(use_case__project=project)
    
    actor_form = ActorForm()
    use_case_form = UseCaseForm()
    transaction_form = TransactionForm()
    
    context = {
        'project': project,
        'actors': actors,
        'use_cases': use_cases,
        'transactions': transactions,
        'actor_form': actor_form,
        'use_case_form': use_case_form,
        'transaction_form': transaction_form,
    }
    
    return render(request, 'project_detail.html', context)


def add_actor(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            actor = form.save(commit=False)
            actor.project = project
            actor.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ActorForm()
    return render(request, 'project_detail.html', {'project': project, 'actor_form': form})

def add_use_case(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = UseCaseForm(request.POST)
        if form.is_valid():
            use_case = form.save(commit=False)
            use_case.project = project
            use_case.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = UseCaseForm()
    return render(request, 'project_detail.html', {'project': project, 'use_case_form': form})

def add_transaction(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            use_case = form.cleaned_data['use_case']
            if use_case.project == project:
                transaction.use_case = use_case
                transaction.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TransactionForm()
    return render(request, 'project_detail.html', {'project': project, 'transaction_form': form})
