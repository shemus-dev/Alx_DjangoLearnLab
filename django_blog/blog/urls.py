from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,add_comment,CommentUpdateView)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/comment/', add_comment, name='add-comment'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('', views.PostListView.as_view(), name='blog-home'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # Search
    path('search/', views.search_posts, name='search'),

    # Tags
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),
    

]
