
from django.test import TestCase
from .models import Post, Profile, Like, Comment

# Create your tests here.
class PostTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.sharry= Profile(user = 'Sharry')

    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.sharry,Profile))