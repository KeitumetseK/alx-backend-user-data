#!/usr/bin/env python3

from flask import request
from typing import List, TypeVar



class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required
        /api/v1/status

        /api/v1/stat*
        ['/api/v1/stat', '']
        """
        if path and not in path.endwith('/'):
            path = path + '/'
        for  excluded_paths in exclude _paths:
            if path.startswith(excluded_path.split('*')[0]):
                return False

        if not path or path not in excluded_paths:
            return True
    
    #Returns True if excluded_paths is None or empty
        if not excluded_paths or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        # If no match is found, authentication is required
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns authorization header
        """

        key = 'Authorization'

        if request is None or key not in request.headers:
            return
        return request.headers.get(key)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user
        """
        return None

