import os
import django

from django.core.wsgi import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akggram.settings')

application = get_default_application()
