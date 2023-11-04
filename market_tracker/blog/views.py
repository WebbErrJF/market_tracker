from django.views.generic import ListView
from .models import Article, Comment
from django.views.generic.detail import DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CommentSerializer, SaveCommentSerializer
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from .forms import ArticleForm


class MainPage(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'blog/article.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        blog_comments = Comment.objects.filter(article_id__id=kwargs['pk']).all()
        serialized_comments = CommentSerializer(blog_comments, many=True)
        context = self.get_context_data(object=self.object, comments=serialized_comments.data, article_id=kwargs['pk'])
        return self.render_to_response(context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blog/article_form.html'
    form_class = ArticleForm

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'blog/article_form.html'
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff


class ArticleDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'blog/delete_confirm.html'
    success_url = 'blog'

    def test_func(self):
        return self.request.user.is_staff


class CommentAPI(APIView):
    http_method_names = ['post', 'patch', 'delete']

    def post(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data['author'] = request.user.id
        serialized_comment = SaveCommentSerializer(data=new_data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        comment_instance = Comment.objects.get(pk=pk)
        serialized_comment = CommentSerializer(comment_instance, data=request.data, partial=True)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment_instance = Comment.objects.get(pk=pk)
        comment_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
