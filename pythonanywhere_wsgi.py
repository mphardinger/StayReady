"""Reference WSGI config for PythonAnywhere. This is NOT auto-loaded by
anything — PythonAnywhere generates its own WSGI file at a fixed path
(/var/www/<username>_pythonanywhere_com_wsgi.py) that you edit through their
dashboard. Copy the contents below into that file (replacing what's there),
swapping <username> for your actual PythonAnywhere username.

Steps to get here: Web tab -> Add a new web app -> Manual configuration ->
Python 3.10 -> click the WSGI configuration file link near the top of the
page to open PythonAnywhere's editor for it.
"""

import sys
import os

# So Python can find app.py, db.py, routes/, etc.
project_dir = '/home/<username>/stayready'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# PythonAnywhere terminates HTTPS for you on the *.pythonanywhere.com
# subdomain — this makes session cookies require it and trusts their proxy
# headers, same as any other host (see app.py).
os.environ['STAYREADY_HTTPS'] = '1'

from app import app as application  # noqa: E402 — must follow the sys.path/env setup above
