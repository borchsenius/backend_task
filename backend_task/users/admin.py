# myapp/admin.py

from django.contrib import admin
import logging

from django.apps import apps

all_models = apps.get_app_config('users').get_models()
logger = logging.getLogger(__name__)

for model in all_models:
    try:
        logger.info("Found model %s", model)
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

