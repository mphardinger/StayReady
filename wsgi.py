"""Production entry point — run Stay Ready behind waitress instead of
Flask's dev server. Set STAYREADY_HTTPS=1 in the host's environment so
session cookies require HTTPS and X-Forwarded-* headers from the host's
TLS-terminating proxy are trusted (see app.py).

Usage: python wsgi.py   (most hosts inject $PORT; defaults to 8008 locally)
"""
import os

from waitress import serve

from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8008))
    print(f'Stay Ready (production) listening on 0.0.0.0:{port}')
    serve(app, host='0.0.0.0', port=port)
