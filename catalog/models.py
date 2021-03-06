import uuid
from datetime import date
from django.contrib.auth.models import User
from django.db import models
# from django.urls import reverse

# Create your models here.
class Genre(models.Model):
    """Model representing book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (ex. Science Fiction).')

    def __str__(self):
        """String representation of Genre object"""
        return self.name

class Language(models.Model):
    """Model representing a language (ex. English, Japanese, Chinese, etc.)"""
    name = models.CharField(max_length=200, help_text='Enter the books natural language.')

    def __str__(self):
        """String representing the Language object"""
        return self.name

class Author(models.Model):
    """Model representing an author."""
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        if self.middle_name:
            return f"{self.last_name}, {self.first_name} {self.middle_name}."
        else:
            return f"{self.last_name}, {self.first_name}"

class Book(models.Model):
    """Model representing a book (general information, NOT rental information)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True) 
    summary = models.TextField(max_length=1000, help_text='Enter a breif description of the book.') 
    isbn = models.CharField(
        'ISBN', 
        max_length=13, 
        unique=True, 
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
        )
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book.')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String representation of Book object."""
        return self.title

    def display_genre(self):
        """Create a string for genre; required to display genre in Admin"""
        return ", ".join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = "Genre"

class BookInstance(models.Model):
    """Model representing a specific copy of a book (ex. of rental stock)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library.')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'set_as_returned'),)

    def __str__(self):
        return f"{self.id} ({self.book.title})"

    @property
    def is_overdue(self):
        """method that checks whether a book is overdue or not"""
        if self.due_back and date.today() > self.due_back:
            return True
        return False