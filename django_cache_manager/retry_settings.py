from django.conf import settings


retry_settings = getattr(settings, 'django_cache_manager_retry_count', 3)
try:
    retry_count = int(retry_settings)
except ValueError:
    retry_count = 3
