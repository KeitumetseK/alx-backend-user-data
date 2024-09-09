#!/usr/bin/env python3
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import IntegrityError


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the provided email and password."""
        try:
            # Check if user with email exists
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except Exception:
            # User does not exist, create new user
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            return False
        except Exception:
            return False

    def _generate_uuid(self) -> str:
        """Generates a new UUID and returns it as a string."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Creates a new session for the user and returns the session ID."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = self._generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
            return None
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Finds user by session ID."""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session by setting the session ID to None."""
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset token for a user."""
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                raise ValueError("User not found")
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception as e:
            raise ValueError("User not found")

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password using a reset token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user is None:
                raise ValueError("Invalid reset token")

            hashed_password = self._hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
        except Exception:
            raise ValueError("Invalid reset token")

