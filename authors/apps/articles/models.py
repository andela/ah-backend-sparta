from django.contrib.postgres import fields
from django.db import models
from django.template.defaultfilters import slugify

from authors.apps.profiles.models import Profile
from authors.apps.authentication.models import User
from django.conf import settings
import math


class Article(models.Model):
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 250)
    slug = models.SlugField(max_length=150)
    body = models.TextField()
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,
     related_name='author')
    tags = fields.ArrayField(models.CharField(max_length=100), blank=True, default=list)
    favorite = models.ManyToManyField(User, related_name='favorite', blank=True, default=False)

    #like-dislike
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        get_latest_by = ['id']

    def get_slug(title):
        """
        create slug from title and adding the id of the article 
        """
        try:
            id=Article.objects.latest().id
            return slugify(title + "-" + str(id))
        except Article.DoesNotExist:
            return slugify(title + "-first")

    @property
    def article_read_time(self):
        """
        Method to calculate article read time
        """
        word_count = 0
        word_count += len(self.body) / int(settings.WORD_LENGTH)
        result = int(word_count / int(settings.WORD_PER_MINUTE))

        read_time =  f"{result} minute read" if result >= 1 else "less than a minute read"
        
        return read_time

    def __str__(self):
        return self.title


class ArticleLikeDislike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    likes = models.BooleanField(default=False, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    


