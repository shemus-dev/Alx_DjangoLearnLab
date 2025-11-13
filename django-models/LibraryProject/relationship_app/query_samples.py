import os
import django

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """Query all books by a specific author using filter()"""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        if books.exists():
            print(f"Books by {author.name}:")
            for book in books:
                print(f"- {book.title}")
        else:
            print(f"No books found for {author.name}.")
    except Author.DoesNotExist:
        print("Author not found.")


def query_books_in_library(library_name):
    """List all books in a specific library using filter()"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Access ManyToMany relationship
        if books.exists():
            print(f"Books in {library.name}:")
            for book in books:
                print(f"- {book.title}")
        else:
            print(f"No books found in {library.name}.")
    except Library.DoesNotExist:
        print("Library not found.")


def query_librarian_for_library(library_name):
    """Retrieve the librarian for a library using Librarian.objects.get(library=...)"""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"The librarian for {library.name} is {librarian.name}.")
    except Library.DoesNotExist:
        print("Library not found.")
    except Librarian.DoesNotExist:
        print("No librarian assigned to this library.")


if __name__ == "__main__":
    query_books_by_author("Chinua Achebe")
    print()
    query_books_in_library("Central Library")
    print()
    query_librarian_for_library("Central Library")
