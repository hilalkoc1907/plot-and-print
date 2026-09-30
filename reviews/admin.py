from django.contrib import admin
from .models import Category, Book, Movie, Review

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Movie)
admin.site.register(Review)