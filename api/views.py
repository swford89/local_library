from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from api.serializers import AuthorSerializer, BookSerializer, BookInstanceSerializer
from catalog.models import Author, Book, BookInstance

class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Authors to be viewed or edited
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Books to be viewed or edited
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookInstanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows BookInstances to be viewed or edited
    """
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]