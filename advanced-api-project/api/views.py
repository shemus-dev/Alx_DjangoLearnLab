from django.shortcuts import render
from rest_framework import generics , permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Book
from rest_framework import status
from rest_framework import filters
from .serializer import BookSerializer


#listview for all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']  # Enables searching by title and author's name
    

# CreateView: Adds a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save() #save object to database

    def create(self, request, *args, **kwargs):
        # This overrides the default method to customize response or validation
        serializer = self.get_serializer(data=request.data)
        #data=request.data: Passes the incoming POST/PUT data to the serializer
        serializer.is_valid(raise_exception=True)  # Validates data according to serializer
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Customize the response
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
        # Customizing validation and response
        partial = kwargs.pop('partial', False)  # Allow PATCH (partial update) if True
        instance = self.get_object()  # Retrieve the object to update
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True) #Validates incoming data; DRF automatically handles errors.
        self.perform_update(serializer)
        return Response(
            {"message": "Book successfully updated", "book": serializer.data},
            status=status.HTTP_200_OK
        )

# DeleteView: Removes a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer  