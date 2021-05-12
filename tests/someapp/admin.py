from django.contrib import admin as dj_admin
from django_neomodel import admin
from .models import Library, Book


class LibraryAdmin(dj_admin.ModelAdmin):
    pass
dj_admin.site.register(Library, LibraryAdmin)


class BookAdmin(admin.ModelAdmin):
    pass
dj_admin.site.register([Book], BookAdmin)
