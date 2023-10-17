from django.views.generic import ListView
from .models import Article
from django.views.generic.detail import DetailView


class MainPage(ListView):
    model = Article
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article.html'
