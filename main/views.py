from django.views.generic import TemplateView, DetailView
from django.db.models import Count, Sum
from projects.models import Project, Category  
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal


def donate_view(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            if amount > 0:
                project.current_amount += amount
                project.save()
                messages.success(request, f"Thanks for donating ${amount:.2f}!")
                return redirect('project_detail', pk=project.pk)
            else:
                messages.error(request, "Amount must be greater than 0.")
        except ValueError:
            messages.error(request, "Invalid amount entered.")

    return render(request, 'components/donation_form.html', {'project': project})


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'components/project_detail.html'  
    context_object_name = 'project'

class HomePage(TemplateView):
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        category_slug = request.GET.get('category')

        project_query = Project.objects.select_related(
            'creator', 'category'
        ).prefetch_related(
            'tags', 'projectpictures_set'
        ).annotate(
            image_count=Count('projectpictures'),
            total_donations=Sum('current_amount'),
        )

        if category_slug:
            project_query = project_query.filter(category__slug=category_slug)

        context['projects'] = project_query.order_by('-start_time')[:10]

        context['categories'] = Category.objects.annotate(
            project_count=Count('project')
        ).order_by('-project_count')[:8]

        context['selected_category'] = category_slug

        return context
