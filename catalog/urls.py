from django.conf.urls import url
from django.urls import path
from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="book_list" ),
    path("book/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("authors/", views.AuthorListView.as_view(), name="author_list"),
    path("author/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
    path("search", views.search, name="search"),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my_borrowed"),
    path("borrowed/", views.LoanedBooksStaffListView.as_view(), name="all_borrowed"),
    path("book/<uuid:pk>/renew/", views.renew_book_librarian, name="renew_book_librarian"),
    path("author/create/", views.AuthorCreate.as_view(), name="author_create"),
    path("author/<int:pk>/update/", views.AuthorUpdate.as_view(), name="author_update"),
    path("author/<int:pk>/delete/", views.AuthorDelete.as_view(), name="author_delete"),
]