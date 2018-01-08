# -*- coding: utf-8 -*-
"""
WSGI config for inspire project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.join(PROJECT_DIR, 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inspire.settings.production")


# activate_this = os.path.join(PROJECT_DIR, 'venv/bin/activate_this.py')
# execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Wrap werkzeug debugger if DEBUG is on
from django.conf import settings
if settings.DEBUG:
    try:
        import django.views.debug
        import six
        from werkzeug.debug import DebuggedApplication

        def null_technical_500_response(request, exc_type, exc_value, tb):
            six.reraise(exc_type, exc_value, tb)

        django.views.debug.technical_500_response = null_technical_500_response
        application = DebuggedApplication(application, evalex=True,
                                          # Turning off pin security as DEBUG is True
                                          pin_security=False)
    except ImportError:
        pass
