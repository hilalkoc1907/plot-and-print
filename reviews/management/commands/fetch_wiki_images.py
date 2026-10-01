from django.core.management.base import BaseCommand
from reviews.models import Book, Movie
from reviews.templatetags.wiki_extras import _find_image


class Command(BaseCommand):
    help = "Kapak resmi olmayan kitap ve filmler için Wikipedia'dan görsel bulup veritabanına kaydeder."

    def handle(self, *args, **options):
        for book in Book.objects.filter(cover_image="", wiki_image_url__isnull=True):
            url = self._lookup(book.title, "novel")
            book.wiki_image_url = url or ""
            book.save(update_fields=["wiki_image_url"])
            self.stdout.write(f"Kitap: {book.title} -> {'bulundu' if url else 'bulunamadı'}")

        for movie in Movie.objects.filter(cover_image="", wiki_image_url__isnull=True):
            url = self._lookup(movie.title, "film")
            movie.wiki_image_url = url or ""
            movie.save(update_fields=["wiki_image_url"])
            self.stdout.write(f"Film: {movie.title} -> {'bulundu' if url else 'bulunamadı'}")

        self.stdout.write(self.style.SUCCESS("Tamamlandı."))

    def _lookup(self, title, hint):
        for lang in ("en", "tr"):
            for term in (f"{title} {hint}".strip(), title):
                url = _find_image(lang, term)
                if url:
                    return url
        return None