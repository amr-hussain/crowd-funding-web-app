from .views import *
from django.urls import path

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('profile/', ProfilePage.as_view(), name='profile'),


    # TODO: Add Views fo thes

    # path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_details'),
    # path('project/<int:pk>/donate/', DonateView.as_view(), name='donate'),
]