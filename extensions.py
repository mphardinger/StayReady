"""Shared Flask extension instances, kept separate from app.py so route
modules can import them without a circular dependency on the app module
(which is also run directly as __main__ via `python app.py`)."""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# In-memory storage: correct as long as this runs as a single process (true
# for waitress here — see wsgi.py). A multi-worker deployment would need a
# shared backend (e.g. Redis) for limits to be enforced consistently.
limiter = Limiter(key_func=get_remote_address, default_limits=['200 per minute'])
