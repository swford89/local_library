from rest_framework import serializers

from catalog.models import Author, Book, BookInstance

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['last_name', 'first_name', 'middle_name']

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'genre', 'language']

class BookInstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookInstance
        fields = ['id', 'book', 'imprint', 'status']