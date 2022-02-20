from django.contrib import admin
from lib_book.models import Library, Book, LibraryActivity, LibraryBook
# Register your models here.

class LibraryModelAdmin(admin.ModelAdmin):
    list_display = ('library_id', 'name', 'city', 'state', 'postal_code')
    list_filter = ('postal_code','city','state',)


class BookModelAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author_name', 'isbn_num', 'genre')
    list_filter = ('genre','author_name',)


class LibraryBookModelAdmin(admin.ModelAdmin):
    list_display = ('library_book_id', 'library_id', 'book_id')
    list_filter = ('library_id',)


class LibraryActivityModelAdmin(admin.ModelAdmin):
    list_display = ('library_activity_id', 'activity_type', 'user', 'library_book_id', 'check_in_at', 'check_out_at')
    readonly_fields = ['check_in_at','check_out_at']
    list_filter = ('activity_type','library_book_id')



admin.site.register(Library, LibraryModelAdmin)
admin.site.register(Book, BookModelAdmin)
admin.site.register(LibraryBook, LibraryBookModelAdmin)
admin.site.register(LibraryActivity, LibraryActivityModelAdmin)