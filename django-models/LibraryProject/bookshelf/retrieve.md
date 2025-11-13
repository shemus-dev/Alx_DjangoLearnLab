### RETRIEVE OPERATION
**Command:**
```python
from bookshelf.models import Book
books = Book.objects.all()
books

book = Book.objects.get(title="1984")
book.title
book.author
book.publication_year

###Expected Outcome

<QuerySet [<Book: 1984 by George Orwell (1949)>]>
'1984'
'George Orwell'
1949
