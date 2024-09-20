from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .filters import PostFilter
from news.models import Post
from .forms import PostNewsForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class PostDetails(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_news'
    model = Post
    form_class = PostNewsForm
    template_name = 'news_create.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.is_post = 'New'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_news'
    model = Post
    form_class = PostNewsForm
    template_name = 'news_edit.html'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_article'
    model = Post
    form_class = PostNewsForm
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.is_post = 'Arc'
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_article'
    model = Post
    form_class = PostNewsForm
    template_name = 'news_edit.html'
