from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.PositiveSmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('postRating'))
        pRat = 0
        pRat += postRat.get('postRating')
        commenRat = self.authorUser.comment_set.aggregate(commentRating=Sum('commentRating'))
        cRat = 0
        cRat += commenRat.get('commentRating')
        self.authorRating = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True, null=True, blank=True)


class Post(models.Model):
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    LENGTH_PREVIEW = 123
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    postTitle = models.CharField(max_length=128)
    postText = models.TextField()
    postRating = models.PositiveSmallIntegerField(default=0)

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        if self.postRating > 0:
            self.postRating -= 1
            self.save()

    def preview(self):
        return f'{self.postText[:self.LENGTH_PREVIEW]}...'


class PostCategory(models.Model):
    postCategory = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    commentText = models.TextField()
    commentRating = models.PositiveSmallIntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        if self.commentRating > 0:
            self.commentRating -= 1
            self.save()
