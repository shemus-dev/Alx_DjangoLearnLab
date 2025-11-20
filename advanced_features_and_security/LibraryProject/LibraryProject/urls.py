from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect 
from bookshelf import views as app_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.login_view, name='root_login'),
    path('', include('bookshelf.urls')),
]
