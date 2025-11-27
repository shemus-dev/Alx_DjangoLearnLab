from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField(auto_now_add=True)
    isbn = models.CharField(max_length=13, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"