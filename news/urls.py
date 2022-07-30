from django.urls import path

from news.views import ListPosts

urlpatterns = [
    path('', ListPosts.as_view()),
]

