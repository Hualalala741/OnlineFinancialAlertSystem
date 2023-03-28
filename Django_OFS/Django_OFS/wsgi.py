"""
WSGI config for Django_OFS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
sys.path.append('D:\github\OnlineFinancialAlertSystem\Django_OFS')
sys.path.append(r'C:\Users\86136\Anaconda3\Lib\site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_OFS.settings')

application = get_wsgi_application()
