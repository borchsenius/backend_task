"""Views for the users app."""

from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext
from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users import serializers


@api_view(["POST"])
def log_in(request) -> Response:
    """Log in the user with the provided credentials."""
    # Make sure required data is sent.
    serializer = serializers.LogInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Try authentication the user.
    user = authenticate(
        request,
        username=serializer.validated_data["email"],
        password=serializer.validated_data["password"],
    )
    if user is None:
        raise exceptions.AuthenticationFailed()

    # Log in the user.
    login(request, user)

    return Response(gettext("You are now logged in."))


@api_view(["POST"])
def log_out(request) -> Response:
    """Log out the current user."""
    logout(request)

    return Response(gettext("You are now logged out."))
