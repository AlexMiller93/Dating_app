from django.test import TestCase

from ..models import User
from .test_views import UserFactory


class UserTestCase(TestCase):
    def test_str(self):
        """Test for string representation."""
        user = UserFactory()
        
        self.assertEqual(str(user), 
            f'{user.first_name} {user.last_name}')