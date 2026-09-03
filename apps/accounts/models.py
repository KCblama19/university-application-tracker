# apps/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for the application tracker.

    We start with Django's AbstractUser so that we retain
    Django's built-in authentication functionality while
    keeping the model easy to extend later.
    """

    email = models.EmailField(
        unique=True,
        help_text="The user's primary email address.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username