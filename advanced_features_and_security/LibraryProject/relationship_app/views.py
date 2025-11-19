from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Book, Library
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.decorators import permission_required
from .forms import BookForm  # You will need a ModelForm for Book
from django.contrib.auth import get_user_model

# ---------------- Authentication Views ----------------
def register(request):
    if request.method == 'POST':
        # Get your CustomUser model
        User = get_user_model()
        
        # Create form and explicitly set the model
        form = UserCreationForm(request.POST)
        form._meta.model = User  # ← EXPLICITLY set the model
        
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
            return redirect('list_books')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        User = get_user_model()
        form = UserCreationForm()
        form._meta.model = User  # ← Also set for GET requests
    
    return render(request, 'relationship_app/register.html', {'form': form})

# relationship_app/views.py
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
                return redirect(role_redirects.get(user.role, 'list_books'))
            return redirect('list_books')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'relationship_app/login.html', {'form': form})

# ADD THIS: Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# ---------------- Book Management ----------------
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect('list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})

# ---------------- Book and Library Views ----------------
@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# ---------------- Role Check Functions - UPDATED ----------------
# UPDATE THESE: Remove UserProfile references
def is_admin(user):
    return user.is_authenticated and user.role == 'Admin'  # ✅ Direct access to role

def is_librarian(user):
    return user.is_authenticated and user.role == 'Librarian'  # ✅ Direct access to role

def is_member(user):
    return user.is_authenticated and user.role == 'Member'  # ✅ Direct access to role

# ---------------- Role-Based Views ----------------
@user_passes_test(is_admin)
@login_required
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
@login_required
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
@login_required
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# ADD THIS: User Profile View
@login_required
def user_profile(request):
    return render(request, 'relationship_app/user_profile.html')