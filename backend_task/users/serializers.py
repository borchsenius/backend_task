"""Serializers for the users app."""

from django.contrib.auth.models import User
from django.utils.translation import gettext
from rest_framework import serializers


class UserAlreadyExistsError(Exception):
    """An exception to raise when trying to create an existing user."""


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        """Meta class for the serializer."""

        fields = ["email", "password"]

    def validate_email(self, value: str) -> None:
        """Make sure we don't already have this user in the system."""
        if User.objects.filter(username=value.lower()).exists():
            raise UserAlreadyExistsError(gettext("This user already exists."))

        return value

    def create(self, validated_data: dict) -> User:
        """Create the user."""
        user = User.objects.create(
            username=validated_data["email"].lower(),
            email=validated_data["email"].lower(),
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class LogInSerializer(serializers.Serializer):
    """A serializer for log in details."""

    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        """Meta class for the serializer."""

        fields = ["email", "password"]


class PasswordResetSerializer(serializers.Serializer):
    """A serializer for password resets."""

    email = serializers.EmailField()

    class Meta:
        """Meta class for the serializer."""

        fields = ["email"]
