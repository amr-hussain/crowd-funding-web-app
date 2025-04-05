
from projects.models import Project
from django.shortcuts import render, redirect
from main.forms import ProjectForm
from main.models import Category
from projects.models import Tag 

def project_list(request):
    projects = Project.objects.select_related('category', 'creator').prefetch_related('tags').all()
    return render(request, 'dashboard/project_list.html', {'projects': projects})


def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  
            project.creator = request.user  
            project.save()
            form.save_m2m()  
            return redirect('project_list')
    else:
        form = ProjectForm()

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'dashboard/project_form.html', {
        'form': form,
        'categories': categories,
        'tags': tags,
    })