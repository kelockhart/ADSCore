# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    entrypoint wsgi script
"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from adscore import app as application

if __name__ == "__main__":

    run_simple(
        '0.0.0.0', 4000, application, use_reloader=False, use_debugger=True
    )
