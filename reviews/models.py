from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kitap Adı")
    author = models.CharField(max_length=200, verbose_name="Yazar")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategori")
    release_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Yayın Yılı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    wiki_image_url = models.URLField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_books', verbose_name="Ekleyen")

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Film Adı")
    director = models.CharField(max_length=200, verbose_name="Yönetmen")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategori")
    release_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Çıkış Yılı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    wiki_image_url = models.URLField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_movies', verbose_name="Ekleyen")

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    RATING_CHOICES = [
        (1, "1 - Çok kötü"),
        (2, "2 - Kötü"),
        (3, "3 - Orta"),
        (4, "4 - İyi"),
        (5, "5 - Mükemmel"),
    ]

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, verbose_name="Puan")
    comment = models.TextField(verbose_name="Yorum")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}/5"