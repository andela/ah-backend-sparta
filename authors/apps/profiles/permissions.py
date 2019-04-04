from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    This method allows only the owner who created a profile to view it
    """

    def has_object_permission(self, request, view, obj):
        """
        This method overrides a method inside the base permission
        """
        if request.method not in SAFE_METHODS:
            # Is the object user the user the same as the object user
            return obj.user == request.user
