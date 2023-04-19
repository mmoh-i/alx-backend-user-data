#!/usr/bin/env python3
"""module for encrypting psskeys
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    ecnrypting pssword
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: string) -> bool:
    """
    validating the provided password to
    match the hashed password.
    """
    return bcypt.checkpw(password.encode('utf-8'), hashed_password)
