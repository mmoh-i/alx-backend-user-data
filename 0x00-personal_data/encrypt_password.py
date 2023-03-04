#!/usr/bin/env python3
import bcrypt


def hash_password(password: str) -> bytes:
    """ecnrypting pssword"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#6. Check valid password
def is_valid(hashed_password: bytes, password: string) -> bool:
    """validating that the provided password
    matches the hashed password."""
    return bcypt.checkpw(password.encode('utf-8'), hashed_password)
