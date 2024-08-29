#!/usr/bin/env python3
"""Module for handling password encryption and validation."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt and return the hashed password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a given password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

