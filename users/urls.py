from .views import *
from django.urls import path , include

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register', register.as_view(), name='register'),
    path('logout', logout_view, name='logout'),
    path ('<int:id>/<str:activation_code>', activation, name='activate'),
    path('active/<int:id>', active, name='active'),
    path ('who', who, name='who'),
    path('delete', delete_user, name='delete'),
    path('tempreport', tempreport, name='delete'),
    path('forget',forget.as_view(), name='forget'),
   
  
]
