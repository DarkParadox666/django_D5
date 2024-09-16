from django.views.generic import ListView, DetailView
from django.shortcuts import render
from news.models import Post, Comment


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 1


class PostDetails(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'



