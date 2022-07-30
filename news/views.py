from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
import django.views.generic as generic


class ListPosts(generic.ListView):
    model = Post
    ordering = 'postAuthor'
    template_name = 'news/posts_list.html'
    context_object_name = 'post_list'
    paginate_by = True


class DetailPost(generic.DetailView):
    model = Post
    ordering = 'postAuthor'
