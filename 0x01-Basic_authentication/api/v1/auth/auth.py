#!/usr/bin/env python3

from flask import request
from typing import List, TypeVar
from api.v1.auth.basic_auth import BasicAuth

BasicAuth = auth

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required
        """
        if path is None:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """ Returns authorization header
        """

        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user
        """
        return None

