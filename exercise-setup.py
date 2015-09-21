"""
Set up fake data for this demo/exercise.

Creates an admin user and enough users to add all the user locations in
'locations.json' (with clone-ish profiles)
"""
import os
import json
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flaregun.settings")
django.setup()

from django.contrib.auth.models import User
from flaregun.api import models

# create an administrator
admin = User.objects.create_superuser('admin', email='admin@admin.net', password='345admin')
admin.save()

# read the locations and create a user and profile for each
with open('locations.json') as locations_file:
    locations_json = locations_file.read()
    locations = json.loads(locations_json)['locations']
    for index, location in enumerate(locations):
        # print index, location

        username = 'user-{}'.format(index)
        user = User.objects.create_user(username, email=(username + '@user.net'), password='123')
        user.save()

        lat, lon = location
        user_location = models.UserLocation( user=user, lat=lat, lon=lon )
        user_location.save()

        user_profile = models.UserProfile( user=user, about=('about: ' + username), favorite_drink='drink')
        user_profile.save()

# for user in User.objects.all():
#     print user
