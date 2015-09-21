from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    """
    Geographic coordinates using latitude and longitude.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # use FloatField for lat/lon instead of DecimalField to be compat with GeoDjango
    lat = models.FloatField()
    lon = models.FloatField()

    class Meta:
        ordering = ('updated',)

    def __str__(self):
        return '{} {}'.format(self.lat, self.lon)
    # TODO: geo uri string


class UserLocation(Location):
    """
    Latitude and longitude for a registered user.
    """
    user = models.OneToOneField(User, related_name="location")
    # TODO: add boolean public - when false, only show to staff/admin


class UserProfile(models.Model):
    """
    A bit of user profile data to display on the map.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, related_name="profile")

    # TODO?: this could be made two fields on the User (or a subclass)
    about = models.CharField(max_length=600)
    favorite_drink = models.CharField(max_length=32)

    class Meta:
        ordering = ('user',)
