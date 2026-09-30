from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Q, F
from .models import Book, Movie, Review, Category


# ---------- ANA SAYFA ----------

class HomeView(TemplateView):
    template_name = 'reviews/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_books'] = Book.objects.annotate(
            avg_rating=Avg('review__rating'), review_count=Count('review')
        ).order_by(F('avg_rating').desc(nulls_last=True), '-review_count')[:4]
        context['top_movies'] = Movie.objects.annotate(
            avg_rating=Avg('review__rating'), review_count=Count('review')
        ).order_by(F('avg_rating').desc(nulls_last=True), '-review_count')[:4]
        context['latest_reviews'] = Review.objects.select_related(
            'user', 'book', 'movie'
        ).order_by('-created_at')[:5]
        context['book_count'] = Book.objects.count()
        context['movie_count'] = Movie.objects.count()
        context['review_count'] = Review.objects.count()
        return context


# ---------- ORTAK: arama/filtre bilgisi + sayfalama linkleri ----------

class FilterContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['q'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        params = self.request.GET.copy()
        params.pop('page', None)
        context['querystring'] = params.urlencode()
        return context


# ---------- KİTAPLAR ----------

class BookListView(FilterContextMixin, ListView):
    model = Book
    template_name = 'reviews/book_list.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        qs = Book.objects.annotate(
            avg_rating=Avg('review__rating'),
            review_count=Count('review'),
        ).order_by('-id')
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(author__icontains=q))
        if category:
            qs = qs.filter(category_id=category)
        return qs


class BookDetailView(DetailView):
    model = Book
    template_name = 'reviews/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(book=self.object).order_by('-created_at')
        context['reviews'] = reviews
        context['avg_rating'] = reviews.aggregate(Avg('rating'))['rating__avg']
        return context


# ---------- FİLMLER ----------

class MovieListView(FilterContextMixin, ListView):
    model = Movie
    template_name = 'reviews/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 6

    def get_queryset(self):
        qs = Movie.objects.annotate(
            avg_rating=Avg('review__rating'),
            review_count=Count('review'),
        ).order_by('-id')
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(director__icontains=q))
        if category:
            qs = qs.filter(category_id=category)
        return qs


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'reviews/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(movie=self.object).order_by('-created_at')
        context['reviews'] = reviews
        context['avg_rating'] = reviews.aggregate(Avg('rating'))['rating__avg']
        return context


# ---------- YORUM EKLEME / DÜZENLEME / SİLME ----------

class BookReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs['pk']})


class MovieReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('movie_detail', kwargs={'pk': self.kwargs['pk']})


class ReviewOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        review = self.get_object()
        if review.book_id:
            return reverse_lazy('book_detail', kwargs={'pk': review.book_id})
        return reverse_lazy('movie_detail', kwargs={'pk': review.movie_id})


class ReviewUpdateView(ReviewOwnerMixin, UpdateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'reviews/review_form.html'


class ReviewDeleteView(ReviewOwnerMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'


# ---------- KAYIT ----------

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)