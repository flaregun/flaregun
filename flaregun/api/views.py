from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from flaregun.api import models
from flaregun.api import serializers
from flaregun.api.permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """API endpoint that allows groups to be viewed or edited."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class UserOwnedViewSet(viewsets.ModelViewSet):
    """
    Viewset that checks whether the request.user matches the 'user' property
    allowing object/owner level permissions.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class UserLocationViewSet(UserOwnedViewSet):
    """API Endpoints for a user's lat/lon location."""
    queryset = models.UserLocation.objects.all()
    serializer_class = serializers.UserLocationSerializer


class UserProfileViewSet(UserOwnedViewSet):
    """API Endpoints for a user's profile data."""
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
