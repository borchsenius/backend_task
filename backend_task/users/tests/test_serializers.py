"""Tests for the serializers of the users app."""

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from users import serializers


class SignUpSerializerTestCase(TestCase):
    """Tests for the sign up serializer."""

    def setUp(self) -> None:
        """Set up some test data."""
        self.existing_user = User.objects.create(
            username="existing@example.com",
            email="existing@example.com",
        )

    def test_sign_up_new_user(self) -> None:
        """Make sure creating a new user works as expected."""
        email = "new@example.com"
        serializer = serializers.SignUpSerializer(
            data={
                "email": email,
                "password": "donttellany1",
            }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, email)

    def test_sign_up_existing_user(self) -> None:
        """Make sure it's not possible to sign up an existing user."""
        serializer = serializers.SignUpSerializer(
            data={
                "email": self.existing_user.email,
                "password": "donttellany1",
            }
        )
        with self.assertRaises(serializers.UserAlreadyExistsError):
            serializer.is_valid(raise_exception=True)


class LogInSerializerTestCase(TestCase):
    """Tests for the log in serializer."""

    def test_fields(self) -> None:
        """Make sure the required fields are there."""
        serializer = serializers.LogInSerializer(
            data={
                "email": "user@example.com",
                "password": "much-secret",
            }
        )
        serializer.is_valid(raise_exception=True)
        self.assertEqual(set(serializer.data.keys()), {"email", "password"})


class PasswordResetSerializerTestCase(TestCase):
    """Tests for the password reset serializer."""

    def test_email_required(self) -> None:
        """Make sure the e-mail field is required."""
        serializer = serializers.PasswordResetSerializer(
            data={
                "animal": "horse",
            }
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
