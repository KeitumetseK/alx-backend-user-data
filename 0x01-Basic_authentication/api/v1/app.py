#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from typing import Literal

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = os.getenv('AUTH_TYPE')

if getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()

if getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> tuple[str, Literal[401]]:
    """ Not authorized handler
    """
    return jsonify ({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> tuple[str, Literal[403]]:
    """ not allowed access to resource
    """
    return jsonify ({"error": "forbidden"}), 403

@app.before_request
def before_request():
    """ Method to filter requests before processing """
    if auth is None:
        return

    # Paths that don't require authentication
    Allowed_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    
    if auth is None:
        return

    if not auth.require_auth(request.path, allowed_paths):
        return

    if auth.authorization_header(request) is None:
        return abort(401)  # Unauthorized

    if auth.current_user(request) is None:
        return abort(403)  # Forbidden

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

@app.route('/api/v1/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

