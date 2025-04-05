from django.contrib import admin
from django.urls import path, include
from main.views import ProjectDetailView  
from main.views import donate_view


urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('chat/', include('chatgpt.urls')),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('donate/<int:pk>/', donate_view, name='donate'),

]

# Serve media files in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
