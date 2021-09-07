from django.shortcuts import render
from catalog.models import Author, Book, BookInstance, Genre, Language

# Create your views here.
def index(request):
    """View for rendering index page"""
    # get count for book and instance objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # available books
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    # get author count
    num_authors = Author.objects.all().count()
    # context dict to pass to template
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
    }
    return render(request, "catalog/index.html", context)

def books_list(request):
    book_list = Book.objects.all()
    context = {"book_list": book_list}
    return render(request, "catalog/books_list.html", context)

def authors_list(request):
    authors_list = Author.objects.all()
    context = {"authors_list": authors_list}
    return render(request, "catalog/authors_list.html", context)

def detail(request):
    return