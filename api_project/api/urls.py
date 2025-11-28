from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList

# router = DefaultRouter()
# router.register('books', BookList)

urlpatterns = [
    # path('', include(router.urls)),
    path('books/', BookList.as_view(), name='book-list'),
]