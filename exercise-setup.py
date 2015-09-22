"""
Set up fake data for this demo/exercise.

Creates an admin user and enough users to add all the user locations in
'locations.json' (with clone-ish profiles)
"""
import os
import random
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flaregun.settings")
django.setup()

from django.contrib.auth.models import User
from flaregun.api import models

# ------------------------------------------------------------------- data
lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum
dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

drinks = [
    "sazerac",
    "whiskey",
    "porter",
    "gin & tonic",
    "reposado tequila",
    "milk",
    "tepid water"
]

# actually airports
cities = {
    "atlanta":      [ 33.69, -84.22 ],
    "austin":       [ 30.3, -97.7 ],
    "chicago":      [ 41.9, -87.65 ],
    "los angeles":  [ 33.93, -118.4 ],
    "new orleans":  [ 29.98, -90.5 ]
}


def generate_random_locations(cities, density=12, variation=0.1):
    def shake(num):
        r = random.random() * variation
        if random.randint(0, 1):
            r = -r
        return num + r

    locations = []
    for name, loc in cities.items():
        count = random.randint(2, density)
        for i in xrange(count):
            new_loc = map(shake, loc)
            locations.append(new_loc)
    return locations

# ------------------------------------------------------------------- models
# create an administrator
admin = User.objects.create_superuser('admin', email='admin@admin.net', password='345admin')
admin.save()

# create the locations and create a user and profile for each
for index, location in enumerate(generate_random_locations(cities, 12)):

    username = 'user-{}'.format(index)
    user = User.objects.create_user(username, email=(username + '@user.net'), password='123')
    user.save()

    lat, lon = location
    user_location = models.UserLocation( user=user, lat=lat, lon=lon )
    user_location.save()

    drink = random.choice(drinks)
    user_profile = models.UserProfile( user=user, about=lorem, favorite_drink=drink)
    user_profile.save()

# for user in User.objects.all():
#     print user
