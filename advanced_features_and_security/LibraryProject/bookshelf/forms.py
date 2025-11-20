from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Exclude created_by since it should be set by the view (request.user)
        exclude = ('created_by',)
