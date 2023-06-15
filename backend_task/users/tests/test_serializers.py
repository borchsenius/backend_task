"""Tests for the serializers of the users app."""

from django.test import TestCase

from users import serializers


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
