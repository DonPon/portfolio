# index/admin.py
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

# Automatically register all models from all installed apps
app_models = apps.get_models()

for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass  # Some models might already be registered, so we skip those
