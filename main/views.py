from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth, TruncMinute, TruncHour
from django.db.models import F
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
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


# class ProfilePage(View):
#     def get(self, request):
#         context = {}
        
#         # Basic user statistics
#         context['user_stats'] = {
#             'total_donated': Donation.objects.aggregate(
#                 total=Sum('amount')
#             )['total'] or 0,
#             'projects_supported': Donation.objects.values(
#                 'project'
#             ).distinct().count(),
#             # 'member_since': "January 2023"  # This should come from user.date_joined
#         }

#         # Monthly donation chart data (last 6 months)
#         six_months_ago = datetime.now() - timedelta(days=180)
#         monthly_donations = Donation.objects.filter(
#             created_at__gte=six_months_ago
#         ).annotate(
#             month=TruncMonth('created_at')
#         ).values('month').annotate(
#             total=Sum('amount')
#         ).order_by('month')

#         context['chart_data'] = {
#             'labels': [d['month'].strftime('%b') for d in monthly_donations],
#             'values': [float(d['total']) for d in monthly_donations]
#         }

#         # Recent donations with project details
#         context['recent_donations'] = Donation.objects.select_related(
#             'project', 'user'
#         ).annotate(
#             project_title=F('project__title'),
#             donation_date=F('created_at'),
#             project_image=F('project__projectpictures__image')
#         ).order_by('-created_at')[:4]

#         # Impact summary
#         context['impact_summary'] = {
#             'annual_target': 100000,  # This should be configurable
#             'current_progress': context['user_stats']['total_donated'],
#             'progress_percentage': min(100, (context['user_stats']['total_donated'] / 100000) * 100),
#         }
#         print("#" * 30, context)
#         return render(request, 'main/profile.html', context)


class ProfilePage(View):
    def get(self, request):
        # Only show the logged-in user's data
        user = request.user
        context = {}
        # user info
        context['user'] = {
            'id': user.id,
            'first_name': user.fname,
            'last_name': user.lname,
            'email': user.email,
            'facebook': user.facebook_acount,
            'birthdate': user.Birthdate,
            'phone': user.phone,
            'is_active': user.active_email,
            'picture_url': user.picture.url if user.picture else 'default.jpg',
            'date_joined': user.date_joined,
            'username': user.username,
        }
        
        # Basic user statistics
        user_donations = Donation.objects.filter(user=user)
        
        context['user_stats'] = {
            'total_donated': user_donations.aggregate(
                total=Sum('amount')
            )['total'] or 0,
            'projects_supported': user_donations.values(
                'project'
            ).distinct().count(),
        }
        ##########################the chart ###########################
        # Get donations for the last 24 hours
        last_24_hours = datetime.now() - timedelta(hours=24)
        
        # Get hourly donations with proper timezone handling
        all_donations = user_donations.filter(
            created_at__gte=last_24_hours
        ).annotate(
            ## we have to remove the tzinfo to match the datetime.now()
            hour=TruncHour('created_at', tzinfo=None)  
        ).values('hour').annotate(
            total=Sum('amount')
        ).order_by('hour')

        print("Donations >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", all_donations)

        # here I created a timeline and truncated anything lower than hour
        all_hours = []
        current = last_24_hours.replace(minute=0, second=0, microsecond=0)  # Normalize to hour start
        end_time = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        while current <= end_time:
            all_hours.append(current)
            current += timedelta(hours=1)

        # create a dictionary of donations by hour 
        donation_dict = {}
        for donation in all_donations:
            hour_key = donation['hour'].replace(tzinfo=None)  # we have to remove the timezone information
            donation_dict[hour_key] = float(donation['total'])

        # Fill in missing hours with zero and create chart data
        context['chart_data'] = {
            'labels': [d.strftime('%H:00') for d in all_hours],
            'values': [donation_dict.get(d, 0) for d in all_hours]
        }

 


        ##############################################################


        # Recent donations with project details
        # Get first image for each project
        recent_donations = user_donations.select_related('project').order_by('-created_at')[:4]
        
        # We need to process the donations to include project images
        donations_with_details = []
        for donation in recent_donations:
            # Get the first image for this project (if any)
            project_image = donation.project.projectpictures_set.first()
            donation_dict = {
                'amount': donation.amount,
                'project_title': donation.project.title,
                'donation_date': donation.created_at,
                'project_image': project_image.image if project_image else None
            }
            donations_with_details.append(donation_dict)
        
        context['recent_donations'] = donations_with_details

        # Calculate category-based impact
        category_donations = user_donations.select_related('project__category').values(
            'project__category__name'
        ).annotate(
            total=Sum('amount')
        )
        
        # Define impact metrics based on categories
        # This is where you'd implement your specific impact calculations
        impacts = []
        for cat_donation in category_donations:
            category = cat_donation['project__category__name']
            amount = cat_donation['total']
            impacts.append({
                'category': category,
                'amount': amount,
            })
            
        
        # Impact summary
        annual_target = 100000  # This should be configurable
        context['impact_summary'] = {
            'annual_target': annual_target,
            'current_progress': context['user_stats']['total_donated'],
            'progress_percentage': min(100, (context['user_stats']['total_donated'] / annual_target) * 100),
            'impacts': impacts
        }


        
    

        for key, value in context.items():
            print(f"{key} ====> : {value}")
        return render(request, 'main/profile.html', context)