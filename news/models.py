from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Юзер')
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

    def __str__(self):
        return f'{self.authorUser.username}'


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.categoryName}'


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
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    postTitle = models.CharField(max_length=128, verbose_name='Название')
    postText = models.TextField(verbose_name='Текст')
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

    def __str__(self):
        return f'{self.postTitle}'


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
