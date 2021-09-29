from django.contrib import admin
from catalog.models import Book, Author, Genre, BookInstance, Language

# Register your models here.

class BookInline(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "middle_name", "date_of_birth", "date_of_death")
    fields = ["last_name", "first_name", "middle_name", ("date_of_birth", "date_of_death")]
    inlines = [BookInline]

admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "borrower", "due_back", "is_overdue", "id")
    list_filter = ("status", "due_back")
    fieldsets = (
        (None,                      {"fields": ("book", "imprint", "id")}),
        ("Availability",            {"fields": ("status", "due_back", "borrower", "is_overdue")}),
    )

admin.site.register(Genre)

admin.site.register(Language)