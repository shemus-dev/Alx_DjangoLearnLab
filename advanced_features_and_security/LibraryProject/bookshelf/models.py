from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver


# ---------------------------
# Existing Models
# ---------------------------

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        # Normalize email (convert to lowercase)
        email = self.normalize_email(email)
        
        # Create user instance
        user = self.model(email=email, **extra_fields)
        
        # Set password (this hashes it properly)
        user.set_password(password)
        
        # Save to database
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        # Set default values for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Set role and membership type for superuser
        extra_fields.setdefault('role', 'Admin')
        extra_fields.setdefault('membership_type', 'admin')
        
        # Validate superuser fields
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
          # Create the superuser using create_user method
        return self.create_user(email, password, **extra_fields)
        

    
#This is the CustomUser model..
class CustomUser(AbstractUser):

    objects = CustomUserManager()   
    # Custom fields
    membership_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('admin', 'Admin')
    ], default='basic')
    date_of_birth = models.DateField(null=True, blank=True,help_text="Format: YYYY-MM-DD")
    profile_photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Make email unique
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'           # Use email as login identifier
    REQUIRED_FIELDS = ['username']  # Username is still required
    
    # Role field
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    class Meta:
        permissions = [
            ("can_access_premium", "Can access premium features"),
            ("can_manage_content", "Can manage all content"),
            ("can_manage_users", "Can manage users"),
        ]

    
    def __str__(self):
        return self.email

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    is_premium = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default =1)

    class Meta:
        permissions = [
            ("can_create_book", "Can create book"),
            ("can_view", "Can view books"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),

            ("can_view_premium_books", "Can view premium books"),
            ("can_publish_book", "Can publish new books"),
            ("can_delete_any_book", "Can delete any book"),
        ]
    def __str__(self):
        return f"{self.title} by {self.author.name}"

   


class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return f"{self.name} ({self.library.name})"


# ---------------------------
# User Profile for Role-Based Access
