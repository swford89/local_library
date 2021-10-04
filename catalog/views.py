import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.views import generic
from catalog.models import Author, Book, BookInstance, Genre

from catalog.forms import RenewBookForm

# index page view.
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

# class-based views
class BookListView(generic.ListView):
    model = Book
    template_name = "catalog/book_list.html"
    paginate_by = 10

class AuthorListView(generic.ListView):
    model = Author
    template_name = "catalog/author_list.html"

class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book_detail.html"

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "catalog/author_detail.html"

# login required
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact="o").order_by("due_back")

# permission required
class LoanedBooksStaffListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_admin.html"
    permission_required = "catalog.can_mark_returned"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")

# searching for book or author
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

# for renewing books
@login_required
@permission_required("catalog.can_mark_returned", raise_exception=True)
def renew_book_librarian(request, pk):
    """function for renewing books"""

    book_instance = get_object_or_404(BookInstance, pk=pk)

    # if recieving a POST request specifying a renewal date
    if request.method == "POST":
        # create form instance
        form = RenewBookForm(request.POST)

        # make sure form is valid
        if form.is_valid():
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()

            return HttpResponseRedirect(reverse("catalog:all_borrowed"))

    # if recieving a GET request and we have to create a renewal date
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

        context = {
            "form": form,
            "book_instance": book_instance,
        }

    return render(request, "catalog/book_renew_librarian.html", context)