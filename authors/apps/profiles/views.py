
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class ProfileCreateAPIView(ListAPIView):
    """
    class to create a profile
    """
    permission_classes = (IsAuthenticated, )
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()




# class ProfileRetrieveAPIView(RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = ProfileSerializer

#     def retrieve(self, request, username, *args, **kwargs):
#         # Try to retrieve the requested profile and throw an exception if the
#         # profile could not be found.
#         try:
#             # We use the `select_related` method to avoid making unnecessary
#             # database calls.
#             profile = Profile.objects.select_related('user').get(
#                 user__username=username
#             )
#         except Profile.DoesNotExist:
#             raise

#         serializer = self.serializer_class(profile)

#         return Response(serializer.data, status=status.HTTP_200_OK)