from django.conf.urls import url
from django.urls import path
from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.books_list, name="books_list" ),
    path("authors/", views.authors_list, name="authors_list"),
    path("book/<int:id>/", views.detail, name="detail"),
    path("author/<int:id>/", views.detail, name="detail"),
]