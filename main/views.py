from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render
from django.db.models import Count, Sum
from projects.models import Project, Category
from interactions.models import Donation, Comment, Rating, Report 
from users.models import User

class HomePage(TemplateView):

    template_name = 'main/home.html'
    
    # fetching some data to display as a starring point....
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured/recent projects with related data
        context['projects'] = Project.objects.select_related(
            'creator', 
            'category'
        ).prefetch_related(
            'tags',
            'projectpictures_set'
        ).annotate(
            image_count=Count('projectpictures'),
            total_donations=Sum('current_amount'),

        ).order_by('-start_time')[:10]

        # Get categories with project counts
        context['categories'] = Category.objects.annotate(
            project_count=Count('project')
        ).order_by('-project_count')[:8]
        
        return context


class ProfilePage(View):
    def get(self, request):
        context = {}
        context['user'] = User.objects.get(pk=self.request.user.pk)
        
        # Get user projects
        context['projects'] = Project.objects.filter(creator=self.request.user).order_by('-start_time')
        return render(request, 'main/profile.html', context)