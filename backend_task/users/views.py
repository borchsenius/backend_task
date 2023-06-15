"""Views for the users app."""

import logging

from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext
from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users import serializers

logger = logging.getLogger(__name__)


@api_view(["POST"])
def sign_up(request) -> Response:
    """Sign up a user."""
    # To not leak whether users already exist in our system, we always give
    # the same response. But, depending on whether it's an existing user or
    # not, we send either a password reset e-mail or a welcome e-mail.
    serializer = serializers.SignUpSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("Send welcome e-mail.")
        # TODO: Send the e-mail.
    except serializers.UserAlreadyExistsError:
        logger.info("Send password reset e-mail instead of welcome e-mail.")
        # TODO: Send the e-mail.

    return Response("ok")


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
