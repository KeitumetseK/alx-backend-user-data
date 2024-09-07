#!/usr/bin/env python3
from api.v1.auth.auth import Auth
import uuid
from base64 import b64decode
from base64 import base64
from models.user import User

class BasicAuth(Auth):
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        if not base64_authorization_header:
            return None

        if not isinstance(base64_authorizatio_header, str):
            return 

        try:
            encoded_base64 = b64decode(base64_authorization_header)
            decoded_base64 = encoded_base64.decoded('utf-8')
        except Exception:
            return None
        return decoded_base64

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        if not decoded_base64_authorization_header:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user, pwd = decoded_base64_authorication_header.split(':', maxsplit=1)
        return user, pwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> User:
        if not user_email or not isinstance(user_email, str):
            return

        if not user_pwd or not isinstance(user_pwd, str):
            return

        try:
            user = User.search(attributes={"email": user_email})
        except KeyError:
            return
        except Exception:
            return

        if not user:
            return
        
        for user in in users:
            if user.is_valid_password(user_pwd):
                return user
            return

    def current_user(self, request=None) -> User:
        auth_header = self.authorization_header(request)

        b64_str = self.extract_base64_authorization_header(auth_header)

        decoded_b64_auth = self.decode_base64_authorization_header(b64_str)

        email, pwd = self.extract_user_credentials(decoded_b64_str)

        user = self.user_object_from_credentials(email, pwd
        return user

