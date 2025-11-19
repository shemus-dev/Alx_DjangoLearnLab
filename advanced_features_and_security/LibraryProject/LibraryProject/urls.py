from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect 
from relationship_app import views as app_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.login_view, name='root_login'),
    path('', include('relationship_app.urls')),
]
