from .views import *
from django.urls import path , include



from main.views import HomePage, UserProjects
from django.contrib.auth import views as auth_views


urlpatterns = [
   
    path('category_list', category_list, name='category_list'),
    path('categories/add/',category_create, name='category_add'),
    path('categories/edit/<int:pk>/',category_update, name='category_edit'),
    path('categories/delete/<int:pk>/',category_delete, name='category_delete'),
    path('projects/', UserProjects.as_view(), name='project_list'), #I need to change this to my-projects url 
    path('projects/add/', project_create, name='project_add'),
    # path('admin_dashboard', AdminDashboardView.as_view(), name='admin_dashboard'),
    # path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),
    # path('edit_user_data', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('export-users/', export_users_csv, name='export_users'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('projects/<int:pk>/edit/', project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', project_delete, name='project_delete'),
    # to toggle the project status
    path('toggle-featured/<int:project_id>/', toggle_featured, name='toggle_featured'),

]