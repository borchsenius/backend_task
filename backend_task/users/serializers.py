"""Serializers for the users app."""

from rest_framework import serializers


class LogInSerializer(serializers.Serializer):
    """A serializer for log in details."""

    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        """Meta class for the serializer."""

        fields = ["email", "password"]
