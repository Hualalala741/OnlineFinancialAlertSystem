#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'Django_OFS.settings'
from django.conf import settings

# Set up Django settings
settings.configure(DEBUG=True)

def main():
    """Run administrative tasks."""

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_OFS.settings')
    import django
    django.setup()
    from django.core.management import execute_from_command_line
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
