"""
Module to define user profile model
"""
from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from simple_history.models import HistoricalRecords


class Comment(models.Model):
    """
    Class to handle creation of user profiles
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default='')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.body

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
