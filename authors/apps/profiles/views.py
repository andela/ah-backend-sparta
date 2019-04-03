
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import(
    AllowAny, IsAuthenticated
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from .renderers import ProfileJSONRenderer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


class ProfileCreateAPIView(ListAPIView):
    """
    class to create a profile
    """
    permission_classes = (AllowAny, )
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def list(self,request, format=None):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(data=dict(profiles=serializer.data), status=status.HTTP_200_OK)


class ProfileDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, )
    queryset = Profile.objects.all()
    renderer_classes = (ProfileJSONRenderer, )
    serializer_class = ProfileSerializer
    lookup_field = 'username'

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), user__username=self.kwargs.get('username')
        )

    def put(self, request, *args, **kwargs):
        profile = self.get_object()

        if profile.user_id != request.user.id:
            return Response(
            data={'message':'You can only edit your Profile'}, 
            status= status.HTTP_403_FORBIDDEN
            )
            
        serializer = self.serializer_class(profile, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(ProfileSerializer(profile).data)
        
    
    
    