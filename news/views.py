from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView


class ListPosts(ListView):
    model = Post
    ordering = 'postAuthor'
    template_name = 'news/product_list.html'
    context_object_name = 'post_list'
    paginate_by = True
