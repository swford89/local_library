import datetime
import uuid

from django.contrib.auth.models import User, Permission
from django.http import response
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

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuserone", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("catalog:my_borrowed"))

        # check that user is logged in
        self.assertEqual(str(response.context["user"]), "testuserone")
        # check for correct response code: 200
        self.assertEqual(response.status_code, 200)
        # check for correct template
        self.assertTemplateUsed(response, "catalog/bookinstance_list_borrowed_user.html")

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username="testuserone", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("catalog:my_borrowed"))

        # chek that user is logged in
        self.assertEqual(str(response.context["user"]), "testuserone")
        # check for correct response code
        self.assertEqual(response.status_code, 200)

        # make sure we don't already have books in list
        self.assertTrue("bookinstance_list" in response.context)
        self.assertEqual(len(response.context["bookinstance_list"]), 0)

        # now change all books to be on loan
        books = BookInstance.objects.all()[:10]

        for book in books:
            book.status = "o"
            book.save()

        response = self.client.get(reverse("catalog:my_borrowed"))
        self.assertEqual(str(response.context["user"]), "testuserone")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("bookinstance_list" in response.context)

        for bookitem in response.context["bookinstance_list"]:
            self.assertEqual(response.context["user"], bookitem.borrower)
            self.assertEqual(bookitem.status, "o")

    def test_pages_ordered_by_due_date(self):
        # change all books to be on-loan
        for book in BookInstance.objects.all():
            book.status = "o"
            book.save()

        login = self.client.login(username="testuserone", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("catalog:my_borrowed"))

        # confirm that only 10 books are displayed due to pagination
        self.assertEqual(str(response.context["user"]), "testuserone")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["bookinstance_list"]), 10)

        last_date = 0
        for book in response.context["bookinstance_list"]:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back

# testing form view
class RenewBookInstanceViewTest(TestCase):

    def setUp(self):
        # create test users
        test_user_one = User.objects.create_user(username="testuserone", password="1X<ISRUkw+tuK")
        test_user_two = User.objects.create_user(username="testusertwo", password="2HJ1vRV0Z&3iD")
        test_user_one.save()
        test_user_two.save()

        # give testusertwo permission to renew books
        permission = Permission.objects.get(name="set_as_returned")
        test_user_two.user_permissions.add(permission)
        test_user_two.save()

        # create book
        test_author = Author.objects.create(first_name="Humble", last_name="Bumble")
        test_genre = Genre.objects.create(name="Non-fiction")
        test_language = Language.objects.create(name="German")
        test_book = Book.objects.create(
            title = "Book Title",
            summary = "Things that really happend, said in a pretty manner.",
            isbn = "XXXXXX",
            author = test_author,
            language = test_language,
        )

        # create genre as post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        # create bookinstance for testuserone
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance_one = BookInstance.objects.create(
            book = test_book,
            imprint = "Super old publisher, 1800",
            due_back = return_date,
            borrower = test_user_one,
            status = "o",
        )

        # create bookinstance for testusertwo
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance_two = BookInstance.objects.create(
            book = test_book,
            imprint = "Another old publisher, 1850",
            due_back = return_date,
            borrower = test_user_two,
            status = "o",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("catalog:renew_book_librarian", kwargs={"pk": self.test_bookinstance_one.pk}))
        # manually check redirect (changes depending on the book on-loan)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username="testuserone", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("catalog:renew_book_librarian", kwargs={"pk": self.test_bookinstance_one.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in__with_permission_borrowed_book(self):
        login = self.client.login(username="testusertwo", password="2HJ1vRV0Z&3iD")
        response = self.client.get(reverse("catalog:renew_book_librarian", kwargs={"pk": self.test_bookinstance_two.pk}))
        # check that it lets us login. This is our book, and we have the right permissions
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username="testusertwo", password="2HJ1vRV0Z&3iD")
        response = self.client.get(reverse("catalog:renew_book_librarian", kwargs={"pk": self.test_bookinstance_one.pk}))
        # check that it lets us login. We're a librarian, so we can view this book
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance
        test_uuid = uuid.uuid4()
        login = self.client.login(username="testusertwo", password="2HJ1vRV0Z&3iD")
        response = self.client.get(reverse("catalog:renew_book_librarian", kwargs={"pk": test_uuid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username="testusertwo", password="2HJ1vRV0Z&3iD")
        response = self.client.get(reverse("catalog:renew_book_librarian", kwargs={"pk": self.test_bookinstance_one.pk}))
        self.assertEqual(response.status_code, 200)
        # check for correct template
        self.assertTemplateUsed(response, "catalog/book_renew_librarian.html")