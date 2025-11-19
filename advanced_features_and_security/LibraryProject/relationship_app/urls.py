from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),  
    path('logout/', views.logout_view, name='logout'),  # ADD THIS
    
    # Book URLs
    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
    # Library URL
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile URL - ADD THIS
    path('profile/', views.user_profile, name='user_profile'),
    
    # Role-based URLs
    path('admin/dashboard/', views.admin_view, name='admin_view'),
    path('librarian/dashboard/', views.librarian_view, name='librarian_view'),
    path('member/dashboard/', views.member_view, name='member_view'),
] 