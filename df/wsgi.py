"""
WSGI config for df project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'df.settings')

application = get_wsgi_application()

#def application(environ, start_response):
#    start_response('200 OK', [('Content-Type', 'text/html')])
#    return ["<h1 style='color:blue'>Hello There!</h1>"]
