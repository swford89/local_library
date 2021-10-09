import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalog.models import Author, Book, BookInstance, Genre, Language

# tesing class-based views
class AuthorListViewTest(TestCase):

    def setUp(self):
        """set up mock data for tests"""
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name = f"Humbolt {author_id}",
                last_name = f"Humberton {author_id}",
            )

    def test_view_url_exists_at_correct_location(self):
        response = self.client.get("/catalog/authors/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_path_name(self):
        response = self.client.get(reverse("catalog:author_list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("catalog:author_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/author_list.html")

    def test_pagination_is_ten(self):
        response = self.client.get(reverse("catalog:author_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["author_list"]), 10)

    def test_lists_all_authors(self):
        # get second page and ensure it has all the remaining authors
        response = self.client.get(reverse("catalog:author_list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["author_list"]), 3)

# tests for login required views
class LoanedBookInstanceByUserListView(TestCase):

    def setUp(self):
        # create two users
        test_user_one = User.objects.create_user(username="testuserone", password="1X<ISRUkw+tuK")
        test_user_two = User.objects.create_user(username="testusertwo", password="2HJ1vRV0Z&3iD")
        test_user_one.save()
        test_user_two.save()

        # create a book
        test_author = Author.objects.create(first_name="Hank", last_name="Hagg")
        test_genre = Genre.objects.create(name="Horror")
        test_language = Language.objects.create(name="Japanese")
        test_book = Book.objects.create(
            title = "Scary Book Title",
            summary = "All the scary details",
            isbn = "XXXXX",
            author = test_author,
            language = test_language,
        )

        # create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        # create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy%5)
            thee_borrower = test_user_one if book_copy % 2 else test_user_two
            status = "m"
            BookInstance.objects.create(
                book = test_book,
                imprint = "Old Publisher, 1800",
                due_back = return_date,
                borrower = thee_borrower,
                status = status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("catalog:my_borrowed"))
        self.assertRedirects(response, "/accounts/login/?next=/catalog/mybooks/")