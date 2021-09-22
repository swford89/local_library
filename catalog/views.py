from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic.list import ListView
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
    # number of genres
    num_genres = Genre.objects.all().count()
    # number of visits, counted with the session variable
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    # context dict to pass to template
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_genres": num_genres,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }
    return render(request, "catalog/index.html", context)

class BookListView(generic.ListView):
    model = Book
    template_name = "catalog/book_list.html"
    paginate_by = 10

# def book_list(request):
#     book_list = Book.objects.all()
#     context = {"book_list": book_list}
#     return render(request, "catalog/book_list.html", context)

class AuthorListView(generic.ListView):
    model = Author
    template_name = "catalog/author_list.html"

# def author_list(request):
#     authors_list = Author.objects.all()
#     context = {"authors_list": authors_list}
#     return render(request, "catalog/author_list.html", context)

class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book_detail.html"

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "catalog/author_detail.html"

# search view
def search(request):
    """searching for book title from search bar"""
    user_search = request.GET['search']
    if user_search:
        books = Book.objects.filter(Q(title__icontains=user_search))
        authors = Author.objects.all().filter(Q(first_name__icontains=user_search))
        context = {
            "books": books,
            "authors": authors,
            }
        return render(request, "catalog/search.html", context)