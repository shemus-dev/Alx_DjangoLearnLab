from django.shortcuts import render
from rest_framework.generics import ListAPIView 
from .models import Book
# Create your views here.
from .serializers import BookSerializer

class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
