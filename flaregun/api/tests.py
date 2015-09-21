import json
import pprint
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from django.contrib.auth.models import User
from . import views
from . import models


def pprint_json(string):
    d = json.loads(string)
    pprint.pprint(d, indent=2)


class UserLocationModelTestCase(TestCase):

    def test_association(self):
        user = User.objects.create_user('waldo')
        user_loc = models.UserLocation(user=user)
        self.assertEqual(user_loc.user, user)


class APITestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser('admin', 'admin@admin.net', '345admin')
        self.admin.save()

    def _create_user_loc(self, username='user', password='123', lat=1.0, lon=2.0):
        """
        Creates and returns a 2-tuple containing a user and location
        associated with that user based on the params given.
        """
        user = User.objects.create_user(username)
        user.save()
        location = models.UserLocation(lat=lat, lon=lon)
        location.user = user
        location.save()
        return (user, location)

    # --------------------------------------------------------------- users
    def test_get_user(self):
        """
        Get /user/{id} should return all user data including:
            * a serialized location
            * a profile
        """
        new_user = User.objects.create_user('new')
        new_user.save()

        location = models.UserLocation(lat=1.23, lon=4.56)
        location.user = new_user
        location.save()

        profile = models.UserProfile(about='I\'m new to the internet!', favorite_drink='milk')
        profile.user = new_user
        profile.save()

        request = self.factory.get('/users/{}/'.format(new_user.pk))
        force_authenticate(request, user=self.admin)

        view = views.UserViewSet.as_view({ 'get' : 'retrieve' })
        response = view(request, pk=new_user.pk).render()
        self.assertEqual(response.status_code, 200)
        # pprint_json(response.content)

        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['location']['lat'], 1.23)
        self.assertEqual(response_dict['location']['lon'], 4.56)
        self.assertEqual(response_dict['profile']['favorite_drink'], 'milk')

    def test_post_user(self):
        """
        Posting to user should create a new user.
        """
        request = self.factory.post('/users/', {
            'username'  : 'test_user',
            'email'     : 'test_user@example.com',
        })
        force_authenticate(request, user=self.admin)

        view = views.UserViewSet.as_view({ 'post' : 'create' })
        response = view(request).render()
        # pprint_json(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)

        # TODO:
        """
        Post /users/ should allow a user to create a user account for themselves.
        """
        """
        Delete /users/{id} will delete the user AND cascade delete the location and profile.
        """
    # --------------------------------------------------------------- locations
    def test_get_locations_unauth(self):
        """
        Get /locations should return all locations
        with no authentication required.
        """
        for x in xrange( 5 ):
            self._create_user_loc(
                username=('user{}'.format(x)),
                lat=(x + 1.0),
                lon=(x + 2.0)
            )

        request = self.factory.get('/locations/')
        view = views.UserLocationViewSet.as_view({ 'get' : 'list' })
        response = view(request).render()
        # pprint_json(response.content)

        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content)
        self.assertEqual(len(response_dict['results']), 5)

    def test_post_location(self):
        """
        Posting to locations should create a new location for a user.
        """
        new_user = User.objects.create_user('new')
        new_user.save()
        request = self.factory.post('/locations/', {
            'user'  : new_user.pk,
            'lat'   : 3.4,
            'lon'   : 5.6,
        })
        force_authenticate(request, user=new_user)

        view = views.UserLocationViewSet.as_view({ 'post' : 'create' })
        response = view(request).render()
        # pprint_json(response.content)

        self.assertEqual(response.status_code, 201)

    def test_post_location_diff_user(self):
        """
        Posting to locations should error if done by a user
        different then the one whose location is being set.
        """
        new_user = User.objects.create_user('new')
        new_user.save()

        user2 = User.objects.create_user('user2')
        user2.save()

        request = self.factory.post('/locations/', {
            'user'  : new_user.pk,
            'lat'   : 3.4,
            'lon'   : 5.6,
        })
        force_authenticate(request, user=user2)

        view = views.UserLocationViewSet.as_view({ 'post' : 'create' })
        response = view(request).render()
        # pprint_json(response.content)

        self.assertNotEqual(response.status_code, 201)

        # TODO:
        """
        Post /locations should create a location
        for the user making the request.
        """

    # --------------------------------------------------------------- profiles
    def test_post_profile(self):
        """
        Posting to locations should create a new location for a user.
        """
        new_user = User.objects.create_user('new')
        new_user.save()
        request = self.factory.post('/profiles/', {
            'user'  : new_user.pk,
            'about' : 'She\'s in a horn-tossing mood.',
            'favorite_drink' : 'Nyquil',
        })
        force_authenticate(request, user=new_user)

        view = views.UserProfileViewSet.as_view({ 'post' : 'create' })
        response = view(request).render()
        # pprint_json(response.content)

        self.assertEqual(response.status_code, 201)
