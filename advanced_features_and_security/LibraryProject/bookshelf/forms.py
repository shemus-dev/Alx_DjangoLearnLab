# bookshelf/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Book, Library
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import re




class SafeSearchForm(forms.Form):
    """Secure search form with input validation"""
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by title, author, or ISBN...',
            'class': 'form-control'
        }),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9\s\-_\.]*$',
                message='Only letters, numbers, spaces, hyphens, dots, and underscores are allowed.'
            )
        ]
    )
    
    category = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Filter by category...',
            'class': 'form-control'
        }),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z\s\-]*$',
                message='Only letters, spaces, and hyphens are allowed for category.'
            )
        ]
    )
    
    min_price = forms.DecimalField(
        required=False, 
        max_digits=6, 
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min price',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    max_price = forms.DecimalField(
        required=False, 
        max_digits=6, 
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Max price',
            'class': 'form-control',
            'step': '0.01'
        })
    )

class BookSearchForm(forms.Form):
    """Simple book search form"""
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search books...',
            'class': 'form-control'
        })
    )
    
    def clean_search_query(self):
        """Sanitize search input"""
        search_query = self.cleaned_data.get('search_query', '')
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[;\\\'"\(\)\-\-]', '', search_query)
        return sanitized.strip()

class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'role')
    
    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class BookForm(forms.ModelForm):
    """Form for creating and updating books"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'description', 'category', 'price', 'is_premium', 'library']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_premium': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'library': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_isbn(self):
        """Validate ISBN format"""
        isbn = self.cleaned_data.get('isbn', '')
        # Basic ISBN validation - remove any hyphens and check length
        clean_isbn = isbn.replace('-', '').replace(' ', '')
        if len(clean_isbn) not in [10, 13]:
            raise forms.ValidationError("ISBN must be 10 or 13 digits long.")
        if not clean_isbn.isdigit():
            raise forms.ValidationError("ISBN must contain only numbers and hyphens.")
        return isbn
    
    def clean_price(self):
        """Validate price"""
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

class LibraryForm(forms.ModelForm):
    """Form for creating and updating libraries"""
    class Meta:
        model = Library
        fields = ['name', 'location', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BookBorrowForm(forms.Form):
    """Form for borrowing books"""
    borrow_days = forms.IntegerField(
        initial=14,
        min_value=1,
        max_value=30,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Number of days to borrow (1-30)"
    )

class ContactForm(forms.Form):
    """Secure contact form"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z\s\-\.]*$',
                message='Name can only contain letters, spaces, hyphens, and dots.'
            )
        ]
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
    
    def clean_name(self):
        """Sanitize name input"""
        name = self.cleaned_data.get('name', '')
        return re.sub(r'[<>{}]', '', name).strip()

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdvancedBookFilterForm(forms.Form):
    """Advanced book filtering form"""
    CATEGORY_CHOICES = [
        ('', 'All Categories'),
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science', 'Science'),
        ('Technology', 'Technology'),
        ('History', 'History'),
        ('Biography', 'Biography'),
        ('Children', 'Children'),
    ]
    
    SORT_CHOICES = [
        ('title', 'Title A-Z'),
        ('-title', 'Title Z-A'),
        ('author', 'Author A-Z'),
        ('-author', 'Author Z-A'),
        ('price', 'Price Low to High'),
        ('-price', 'Price High to Low'),
        ('-created_at', 'Newest First'),
    ]
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    show_premium = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Include Premium Books'
    )

# If you need an ExampleForm for testing, here it is:
class ExampleForm(forms.Form):
    """Example form for demonstration purposes"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your message'})
    )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name