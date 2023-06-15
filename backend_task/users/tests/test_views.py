"""Tests for the views of the users app."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class SignUpTestCase(TestCase):
    """Tests for the sign up view."""

    def setUp(self) -> None:
        """Set up some test data."""
        self.client = APIClient()
        self.user = User.objects.create(
            username="existing@example.com",
            email="existing@example.com",
        )

    def test_successful_sign_up(self) -> None:
        """Make sure it's possible to sign up new users."""
        user_count = User.objects.count()
        response = self.client.post(
            reverse("users:sign-up"),
            {
                "email": "new@example.com",
                "password": "1234horse",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_signing_up_existing_user(self) -> None:
        """Make sure it's not possible to sign up existing users."""
        user_count = User.objects.count()
        response = self.client.post(
            reverse("users:sign-up"),
            {
                "email": self.user.email,
                "password": "1234horse",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), user_count)


class LogInTestCase(TestCase):
    """Tests for the log in view."""

    def setUp(self) -> None:
        """Set up some test data."""
        self.client = APIClient()
        self.user = User.objects.create(
            username="existing@example.com",
            email="existing@example.com",
        )
        self.password = "much-secret"
        self.user.set_password(self.password)
        self.user.save()

    def test_correct_password(self) -> None:
        """Make sure it's possible to log in with the correct password."""
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(
            reverse("users:log-in"),
            {
                "email": self.user.email,
                "password": self.password,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_wrong_password(self) -> None:
        """Make sure using a wrong password does not log you in."""
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(
            reverse("users:log-in"),
            {
                "email": self.user.email,
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_unknown_user(self) -> None:
        """Make sure unknown users are not logged in."""
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(
            reverse("users:log-in"),
            {
                "email": "unknown@example.com",
                "password": self.password,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_missing_field(self) -> None:
        """Make sure leaving out the password gives a validation error."""
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(
            reverse("users:log-in"),
            {
                "email": self.user.email,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("_auth_user_id", self.client.session)


class LogOutTestCase(TestCase):
    """Tests for the log out view."""

    def setUp(self) -> None:
        """Set up some test data."""
        self.client = APIClient()
        self.user = User.objects.create(
            username="existing@example.com",
            email="existing@example.com",
        )
        self.client.force_login(self.user)

    def test_log_out(self) -> None:
        """Make sure logging out works."""
        self.assertIn("_auth_user_id", self.client.session)
        response = self.client.post(reverse("users:log-out"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("_auth_user_id", self.client.session)


class PasswordResetTestCase(TestCase):
    """Tests for the password reset."""

    def setUp(self) -> None:
        """Set up some test data."""
        self.client = APIClient()
        self.user = User.objects.create(
            username="existing@example.com",
            email="existing@example.com",
        )

    def test_reset_for_known_and_unknown(self):
        """Make sure password reset does not leak information about users."""
        # First we make a reset request for our known user and expect a
        # good response.
        response_for_known = self.client.post(
            reverse("users:reset-password"),
            data={
                "email": self.user.email,
            },
        )
        self.assertEqual(response_for_known.status_code, status.HTTP_200_OK)

        # Now make a request for an unknown user. We expect the response to
        # be identical to the one for the known user.
        response_for_unknown = self.client.post(
            reverse("users:reset-password"),
            data={
                "email": "unknown@example.com",
            },
        )
        self.assertEqual(
            response_for_known.status_code,
            response_for_unknown.status_code,
        )
        self.assertEqual(
            response_for_known.json(),
            response_for_unknown.json(),
        )
