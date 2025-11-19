# relationship_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, Author

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'membership_type', 'is_staff')
    list_filter = ('membership_type', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Membership', {'fields': ('membership_type',)}),
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_premium', 'created_by')
    list_filter = ('is_premium',)
    search_fields = ('title', 'author')


