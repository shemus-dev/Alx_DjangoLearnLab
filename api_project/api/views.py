from django.shortcuts import render
from rest_framework.generics import ListAPIView 
from rest_framework import viewsets
from .models import Book
# Create your views here.
from .serializers import BookSerializer

class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer   
