#!/usr/bin/env python3

from flask import request
from typing import List, TypeVar



class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required
        """
        if path is None or not excluded_paths:
            return True

        # Normalize the path to handle trailing slashes (optional)
        if path[-1] == '/':
            path = path[:-1]

        for excluded_path in excluded_paths:
            # Remove trailing slash from excluded_path if it exists
            if excluded_path[-1] == '/':
                excluded_path = excluded_path[:-1]

            # Handle wildcard matches, such as "/api/v1/stat*"
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                # Exact match check
                if path == excluded_path:
                    return False

        # If no match is found, authentication is required
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns authorization header
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user
        """
        return None

