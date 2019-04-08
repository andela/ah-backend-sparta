from django.db import models
from django.utils import timezone
from authors.apps.authentication.models import User
from django.template.defaultfilters import slugify
from authors.apps.profiles.models import Profile

class Article(models.Model):
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 250)
    slug = models.SlugField(max_length=150)
    body = models.TextField()
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,
     related_name='author')

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

    def __str__(self):
        return self.title


