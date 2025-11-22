from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Exclude created_by since it should be set by the view (request.user)
        exclude = ('created_by',)

class SafeSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search books...'})
    )
    category = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Category'})
    )
    min_price = forms.DecimalField(
        required=False, 
        max_digits=6, 
        decimal_places=2,
        min_value=0
    )
    max_price = forms.DecimalField(
        required=False, 
        max_digits=6, 
        decimal_places=2,
        min_value=0
    )


