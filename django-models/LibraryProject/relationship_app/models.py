from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver


# ---------------------------
# Existing Models
# ---------------------------
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
#This is the CustomUser model..
class CustomUser(AbstractUser):
    # Custom fields
    membership_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('admin', 'Admin')
    ], default='basic')
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Make email unique
    email = models.EmailField(unique=True)
    
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
        ]

    
    def __str__(self):
        return self.email



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    is_premium = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default =1)

    class Meta:
        permissions = [
            ("can_view_premium_books", "Can view premium books"),
            ("can_publish_book", "Can publish new books"),
            ("can_delete_any_book", "Can delete any book"),
        ]

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]


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
