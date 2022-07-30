from django.urls import path

from news.views import ListPosts, DetailPost

urlpatterns = [
    path('', ListPosts.as_view()),
    path('<int:pk>', DetailPost.as_view()),
]

