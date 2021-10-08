import datetime

from django.test import TestCase

from catalog.models import Author

class AuthorModelTest(TestCase):

    def setUp(self):
        """set up non-modified objects used by all test methods"""
        Author.objects.create(first_name="Hugh", last_name="Humber", date_of_birth=datetime.date(1989, 9, 27), date_of_death=datetime.date(2020, 8, 26))

    def test_first_name_label(self):
        author = Author.objects.get(first_name="Hugh")
        field_label = author._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_last_name_label(self):
        author = Author.objects.get(first_name="Hugh")
        field_label = author._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_date_of_birth_label(self):
        author = Author.objects.get(first_name="Hugh")
        field_label = author._meta.get_field("date_of_birth").verbose_name
        self.assertEqual(field_label, "date of birth")

    def test_date_of_death_label(self):
        author = Author.objects.get(first_name="Hugh")
        field_label = author._meta.get_field("date_of_death").verbose_name
        self.assertEqual(field_label, "Died")

    def test_first_name_max_length(self):
        author = Author.objects.get(first_name="Hugh")
        max_length = author._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(first_name="Hugh")
        expected_object_name = f"{author.last_name}, {author.first_name}"
        self.assertEqual(str(author), expected_object_name)