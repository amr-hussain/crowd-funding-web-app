from users.views import home
from django.urls import path , include
from users.views import * 
urlpatterns = [
    # path('', home, name='home'),
    path('login', login.as_view(), name='login'),
    path('test', test.as_view(), name='test'),
]
