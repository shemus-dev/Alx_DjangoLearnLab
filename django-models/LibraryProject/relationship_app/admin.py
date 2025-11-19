# relationship_app/admin.py - SIMPLER VERSION
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Basic list display
    list_display = ('username', 'email', 'role', 'membership_type', 'is_staff')
    
    # Basic filters
    list_filter = ('role', 'membership_type', 'is_staff')
    
    # Basic search
    search_fields = ('username', 'email')
    
    # Simple fieldsets for editing
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': (
                'date_of_birth',
                'profile_photo', 
                'phone_number',
                'bio',
                'role',
                'membership_type'
            )
        }),
    )
    
    # Simple add fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': (
                'date_of_birth',
                'phone_number',
                'role',
                'membership_type'
            )
        }),
    )

# Register your other models normally
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Library)
admin.site.register(Librarian)