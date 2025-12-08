from django.shortcuts import render
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from .models import Book
from .serializer import BookSerializer


# ListView for all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
    filter_backends = [
        django_filters.DjangoFilterBackend,  #  field filtering
        filters.SearchFilter,                 #  search
        filters.OrderingFilter,               #  sorting
    ]
    
    # fields can be filtered
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'author': ['exact', 'icontains'],
        'published_year': ['exact', 'gte', 'lte'],  # Use your actual field name
    }
    
    # Search fields - works with ?search=query
    search_fields = ['title', 'author__name', 'publication_year']
    
    # Define which fields can be used for sorting
    ordering_fields = ['title', 'published_year', 'author']  # Use actual field name
    ordering = ['title']  # Default ordering
    
    # Allow anyone to view
    permission_classes = [permissions.AllowAny]


# CreateView: Adds a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()  # Save object to database

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {"message": "Book successfully created", "book": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


# UpdateView: Modifies an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {"message": "Book successfully updated", "book": serializer.data},
            status=status.HTTP_200_OK
        )


# DeleteView: Removes a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        
        return Response(
            {"message": f"Book '{book_title}' successfully deleted"},
            status=status.HTTP_200_OK
        )


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]