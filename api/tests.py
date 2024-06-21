# /mnt/data/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Sucursal

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.sucursal = Sucursal.objects.create(nombre="Sucursal 1", direccion="Dirección 1")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.profile = Profile.objects.create(user=self.user, rol="vendedor", sucursal=self.sucursal)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.rol, "vendedor")
        self.assertEqual(self.profile.sucursal, self.sucursal)
