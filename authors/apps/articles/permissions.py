from rest_framework import permissions
from .models import Article
from authors.apps.profiles.models import Profile


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        profile = Profile.objects.filter(user=request.user).first()
        user = Article.objects.filter(author=profile).first()
        return obj.author == profile

