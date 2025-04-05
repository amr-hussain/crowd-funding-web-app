# from .views import HomePage
# from django.urls import path
#
# urlpatterns = [
#     path('', HomePage.as_view(), name='home'),
#
#
#     # TODO: Add Views fo thes
#
#     # path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_details'),
#     # path('project/<int:pk>/donate/', DonateView.as_view(), name='donate'),
# ]


from django.urls import path
from .dashboard import category_views  # if using a subfolder
from .views import HomePage
from django.contrib.auth import views as auth_views
from .dashboard import project_views

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('dashboard/categories/', category_views.category_list, name='category_list'),
    path('dashboard/categories/add/', category_views.category_create, name='category_add'),
    path('dashboard/categories/edit/<int:pk>/', category_views.category_update, name='category_edit'),
    path('dashboard/categories/delete/<int:pk>/', category_views.category_delete, name='category_delete'),
    path('dashboard/projects/', project_views.project_list, name='project_list'),
    path('dashboard/projects/add/', project_views.project_create, name='project_add'),

]
