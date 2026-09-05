from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserModelTests(TestCase):
    """Tests for the custom User model."""

    def test_user_can_be_created(self):
        """A user can be created with valid account information."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="User",
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

    def test_password_is_hashed(self):
        """Passwords are stored as hashes rather than plain text."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        self.assertNotEqual(user.password, "TestPassword123!")
        self.assertTrue(user.check_password("TestPassword123!"))