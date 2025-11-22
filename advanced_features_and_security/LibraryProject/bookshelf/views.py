from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Book, Library
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import get_user_model
from .forms import (BookForm, SafeSearchForm, BookSearchForm, CustomUserCreationForm,
                   LibraryForm, BookBorrowForm, ContactForm, UserProfileForm,
                   AdvancedBookFilterForm, ExampleForm  
)
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.exceptions import PermissionDenied

# --- ADD MISSING HELPER FUNCTION ---
def redirect_to_dashboard(user):
    """Helper function to redirect users based on their role"""
    if hasattr(user, 'role'):
        if user.role == 'Admin':
            return redirect('admin_view')
        elif user.role == 'Librarian':
            return redirect('librarian_view')
        elif user.role == 'Member':
            return redirect('member_view')
    return redirect('book_list')

# ---------------- Authentication Views ----------------
def register(request):
    if request.method == 'POST':
        # FIXED: Use CustomUserCreationForm instead of UserCreationForm
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            
            # Your role-based redirect logic
            if hasattr(user, 'role'):
                if user.role == 'Admin':
                    return redirect('admin_view')
                elif user.role == 'Librarian':
                    return redirect('librarian_view')
                elif user.role == 'Member':
                    return redirect('member_view')
            return redirect('book_list')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        # FIXED: Use CustomUserCreationForm instead of UserCreationForm
        form = CustomUserCreationForm()
    
    return render(request, 'bookshelf/register.html', {'form': form})

def login_view(request):
    """
    Most efficient login view
    """
    # Redirect already logged-in users who manually visit /login/
    if request.user.is_authenticated and request.path == '/login/':
        return redirect_to_dashboard(request.user)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            # Direct role-based redirect
            if hasattr(user, 'role'):
                role_redirects = {
                    'Admin': 'admin_view',
                    'Librarian': 'librarian_view', 
                    'Member': 'member_view'
                }
                return redirect(role_redirects.get(user.role, 'book_list'))
            return redirect('book_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'bookshelf/login.html', {'form': form})

# ADD THIS: Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# ---------------- Book Management ----------------
@permission_required('bookshelf.can_create_book', raise_exception=True)  # FIXED: Removed extra quote
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect('book_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_change_book', raise_exception=True)
def edit_book(request, pk):
    # SECURE: Use get_object_or_404 instead of direct get()
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect('book_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    # SECURE: Use get_object_or_404 instead of direct get()
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# ---------------- Book and Library Views ----------------
@login_required
def book_list(request):
    # SECURE: Using Django ORM with safe filtering
    books = Book.objects.all()
    
    # REASON: Filter out premium books if user doesn't have premium permission
    if not request.user.has_perm('bookshelf.can_view_premium_books'):
        books = books.filter(is_premium=False)
    
    # ADDED: Safe search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        # SECURE: Use Django ORM with parameterized queries
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query,
    })

# ADDED: Example view using ExampleForm
@login_required
def example_form_view(request):
    """Example view demonstrating the use of ExampleForm"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Process the form data (in a real app, you might save to database, send email, etc.)
            messages.success(request, f"Thank you {name}! Your message has been received.")
            return redirect('book_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})

# REASON: Class-based views need method_decorator for permission checks
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('bookshelf.can_view', raise_exception=True), name='dispatch')
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'bookshelf/library_detail.html'
    context_object_name = 'library'

# ---------------- Role Check Functions - UPDATED ----------------
def is_admin(user):
    return user.is_authenticated and user.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.role == 'Member'

# ---------------- Role-Based Views ----------------
@user_passes_test(is_admin)
@permission_required('bookshelf.can_manage_content', raise_exception=True)
@login_required
def admin_view(request):
    total_books = Book.objects.count()
    premium_books = Book.objects.filter(is_premium=True).count()
    context = {
        'total_books': total_books,
        'premium_books': premium_books,
    }
    return render(request, 'bookshelf/admin_view.html', context)

@user_passes_test(is_librarian)
@login_required
def librarian_view(request):
    return render(request, 'bookshelf/librarian_view.html')

@user_passes_test(is_member)
@login_required
def member_view(request):
    # FIXED: Corrected Book.filter to Book.objects.filter
    if request.user.has_perm('bookshelf.can_view_premium_books'):
        books = Book.objects.all()
    else:
        books = Book.objects.filter(is_premium=False)

    context = {'books': books}
    return render(request, 'bookshelf/member_view.html', context)

# ADD THIS: User Profile View
@login_required
def user_profile(request):
    return render(request, 'bookshelf/user_profile.html')