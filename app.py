import os
import secrets
from datetime import timedelta

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from db import DATA_DIR, close_db, init_db
from extensions import limiter

# Set by the production host (NOT for local/LAN dev — leaving this unset keeps
# session cookies working over plain HTTP for phone/LAN testing). When set,
# the app trusts one hop of X-Forwarded-* headers from a TLS-terminating
# reverse proxy (the host's load balancer) and requires HTTPS for cookies.
IS_PRODUCTION = os.environ.get('STAYREADY_HTTPS') == '1'


def _secret_key():
    """Persist a random secret so sessions survive server restarts."""
    path = os.path.join(DATA_DIR, 'instance', 'secret_key.txt')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    key = secrets.token_hex(32)
    with open(path, 'w') as f:
        f.write(key)
    return key


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.secret_key = _secret_key()
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = IS_PRODUCTION
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

    if IS_PRODUCTION:
        # Trust X-Forwarded-For/Proto from exactly one reverse-proxy hop (the
        # host's edge) so request.is_secure and the client IP used for rate
        # limiting reflect the real client, not the proxy.
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

    init_db()
    app.teardown_appcontext(close_db)
    limiter.init_app(app)

    from routes.auth import bp as auth_bp
    from routes.members import bp as members_bp
    from routes.pantry import bp as pantry_bp
    from routes.recipes import bp as recipes_bp
    from routes.plan import bp as plan_bp
    from routes.shopping import bp as shopping_bp
    from routes.calendar_export import bp as calendar_bp
    from routes.household import bp as household_bp
    from routes.balance import bp as balance_bp
    for bp in (auth_bp, members_bp, pantry_bp, recipes_bp, plan_bp, shopping_bp,
               calendar_bp, household_bp, balance_bp):
        app.register_blueprint(bp)

    @app.get('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.errorhandler(404)
    def not_found(_e):
        if request.path.startswith('/api/'):
            return jsonify(error='Not found'), 404
        return send_from_directory(app.static_folder, 'index.html')

    @app.errorhandler(500)
    def server_error(_e):
        return jsonify(error='Something went wrong on the server'), 500

    @app.errorhandler(429)
    def rate_limited(_e):
        return jsonify(error='Too many attempts — wait a bit and try again'), 429

    return app


app = create_app()

if __name__ == '__main__':
    # 0.0.0.0 so phones on the same WiFi can reach it too, not just this PC.
    # Fine for home-network testing; use a real WSGI server + HTTPS before
    # exposing this beyond your own LAN.
    print('Stay Ready is cooking at http://127.0.0.1:8008')
    print('On your phone (same WiFi): http://<this-PCs-LAN-IP>:8008')
    app.run(host='0.0.0.0', port=8008)
