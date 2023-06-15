"""URLs for the users app."""

from django.urls import path

from users import views

urlpatterns = [
    path("log-in/", views.log_in, name="log-in"),
    path("log-out/", views.log_out, name="log-out"),
]
