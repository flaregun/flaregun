from django.contrib.auth.models import User, Group
from flaregun.api import models
from rest_framework import serializers


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserLocation
        fields = ('id', 'url', 'lat', 'lon', 'user')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'url', 'about', 'favorite_drink', 'user')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class NestedUserLocationSerializer(serializers.ModelSerializer):
        """For nested display inside user json (no user or url)."""
        class Meta:
            model = models.UserLocation
            fields = ('id', 'lat', 'lon')

    class NestedUserProfileSerializer(serializers.ModelSerializer):
        """For nested display inside user json (no user or url)."""
        class Meta:
            model = models.UserProfile
            fields = ('id', 'about', 'favorite_drink')

    #: reverse relation for lat-lon user locations
    location = NestedUserLocationSerializer(allow_null=True, read_only=True)
    #: reverse relation for profile data/blurb
    profile = NestedUserProfileSerializer(allow_null=True, read_only=True)

    class Meta:
        model = User
        # note: do not expose email
        fields = ('id', 'url', 'username', 'location', 'profile')
        # TODO: expose email to admin users

    def create(self, validated_data):
        """
        Override to pull location and profile nested data out
        and instantiate them separately.
        """
        location_data = validated_data.pop('location', None)
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create(**validated_data)

        if location_data:
            models.UserLocation.objects.create(user=user, **location_data)
        if profile_data:
            models.UserProfile.objects.create(user=user, **profile_data)

        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'url', 'name')
