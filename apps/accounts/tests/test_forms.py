from django.test import TestCase

from apps.accounts.forms import RegisterForm
from apps.accounts.models import User


class RegisterFormTests(TestCase):
    """Tests for the user registration form."""

    def test_valid_registration_form(self):
        """A valid registration form creates an account."""
        form = RegisterForm(
            data={
                "username": "testuser",
                "email": "TEST@EXAMPLE.COM",
                "first_name": "Test",
                "last_name": "User",
                "password": "TestPassword123!",
                "password_confirmation": "TestPassword123!",
            }
        )

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(
            user.check_password("TestPassword123!")
        )

    def test_email_is_normalized(self):
        """Email addresses are stored in lowercase."""
        form = RegisterForm(
            data={
                "username": "testuser",
                "email": "  TEST@EXAMPLE.COM  ",
                "first_name": "Test",
                "last_name": "User",
                "password": "TestPassword123!",
                "password_confirmation": "TestPassword123!",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["email"],
            "test@example.com",
        )

    def test_duplicate_email_is_rejected(self):
        """An email address already in use cannot register again."""
        User.objects.create_user(
            username="existinguser",
            email="test@example.com",
            password="TestPassword123!",
        )

        form = RegisterForm(
            data={
                "username": "newuser",
                "email": "TEST@EXAMPLE.COM",
                "first_name": "New",
                "last_name": "User",
                "password": "TestPassword123!",
                "password_confirmation": "TestPassword123!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_password_confirmation_must_match(self):
        """Registration fails when the passwords do not match."""
        form = RegisterForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "TestPassword123!",
                "password_confirmation": "DifferentPassword123!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "password_confirmation",
            form.errors,
        )
        
    def test_duplicate_username_is_rejected(self):
        """A username already in use cannot be registered again."""
        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="TestPassword123!",
        )

        form = RegisterForm(
            data={
                "username": "existinguser",
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "password": "TestPassword123!",
                "password_confirmation": "TestPassword123!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)