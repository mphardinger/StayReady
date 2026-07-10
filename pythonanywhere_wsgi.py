"""Reference WSGI config for PythonAnywhere. This file is NOT auto-loaded by
anything — PythonAnywhere generates its own WSGI file at a fixed path
(/var/www/stayready_pythonanywhere_com_wsgi.py) that you edit through the Web
tab. Copy the code below (everything under the docstring) into that file,
replacing whatever PythonAnywhere put there.

To get there: Web tab -> Add a new web app -> Manual configuration ->
Python 3.10 -> click the "WSGI configuration file" link near the top of the
page to open PythonAnywhere's editor for it.
"""

import sys
import os

# So Python can find app.py, db.py, routes/, etc. This assumes you cloned the
# repo into ~/stayready:  git clone <repo-url> stayready
project_dir = '/home/StayReady/stayready'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# PythonAnywhere terminates HTTPS for you on the *.pythonanywhere.com
# subdomain — this makes session cookies require it and trusts their proxy
# headers, same as any other production host (see app.py's IS_PRODUCTION).
os.environ['STAYREADY_HTTPS'] = '1'

from app import app as application  # noqa: E402 — must follow the sys.path/env setup above
