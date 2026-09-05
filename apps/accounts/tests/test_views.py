from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class LoginViewTests(TestCase):
    """Tests for the user login view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

    def test_login_page_is_accessible(self):
        """The login page is available to unauthenticated users."""
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_valid_login_authenticates_user(self):
        """Valid credentials log the user in."""
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "testuser",
                "password": "TestPassword123!",
            },
        )

        self.assertRedirects(
            response,
            reverse("dashboard:home"),
        )

        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )

    def test_invalid_login_is_rejected(self):
        """Invalid credentials do not authenticate the user."""
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "testuser",
                "password": "WrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

        self.assertContains(
            response,
            "Invalid username or password.",
        )

    def test_authenticated_user_is_redirected_from_login(self):
        """Authenticated users are redirected away from the login page."""
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:login")
        )

        self.assertRedirects(
            response,
            reverse("dashboard:home"),
        )
        
    def test_login_redirects_to_next_url(self):
        """A valid login redirects to the requested next URL."""
        response = self.client.post(
            reverse("accounts:login") + "?next=/applications/",
            {
                "username": "testuser",
                "password": "TestPassword123!",
            },
        )

        self.assertRedirects(
            response,
            "/applications/",
        )


class LogoutViewTests(TestCase):
    """Tests for the user logout view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

    def test_authenticated_user_can_logout(self):
        """An authenticated user is logged out successfully."""
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:logout")
        )

        self.assertRedirects(
            response,
            reverse("accounts:login"),
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_logout_requires_authentication(self):
        """Unauthenticated users cannot access the logout view."""
        response = self.client.get(
            reverse("accounts:logout")
        )

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            reverse("accounts:login"),
            response.url,
        )

    def test_logout_displays_success_message(self):
        """Logging out adds the expected success message."""
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:logout")
        )

        messages = list(
            get_messages(response.wsgi_request)
        )

        self.assertTrue(
            any(
                str(message)
                == "You have been logged out successfully."
                for message in messages
            )
        )


class RegisterViewTests(TestCase):
    """Tests for the user registration view."""

    def test_register_page_is_accessible(self):
        """The registration page is available to visitors."""
        response = self.client.get(
            reverse("accounts:register")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/register.html",
        )

    def test_valid_registration_creates_user(self):
        """Valid registration data creates a new account."""
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "password": "TestPassword123!",
                "password_confirmation": "TestPassword123!",
            },
        )

        self.assertRedirects(
            response,
            reverse("dashboard:home"),
        )

        self.assertTrue(
            User.objects.filter(
                username="newuser"
            ).exists()
        )

    def test_registration_logs_user_in(self):
        """A newly registered user is automatically authenticated."""
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "password": "TestPassword123!",
                "password_confirmation": "TestPassword123!",
            },
        )

        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )

        self.assertEqual(
            response.wsgi_request.user.username,
            "newuser",
        )

    def test_authenticated_user_is_redirected_from_register(self):
        """Authenticated users are redirected away from registration."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        self.client.force_login(user)

        response = self.client.get(
            reverse("accounts:register")
        )

        self.assertRedirects(
            response,
            reverse("dashboard:home"),
        )

    def test_invalid_registration_does_not_create_user(self):
        """Invalid registration data does not create an account."""
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "password": "TestPassword123!",
                "password_confirmation": "DifferentPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            User.objects.filter(
                username="newuser"
            ).exists()
        )