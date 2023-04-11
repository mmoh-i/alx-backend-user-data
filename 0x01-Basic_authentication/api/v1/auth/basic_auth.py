#!/usr/bin/env python3
"""Basic authentication module
to inherit from auth
"""
from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar
import base64


class BasicAuth(Auth):
    """
    Class that implements Basic Authentication.
    Inherits from Auth.
    """
    def extract_base64_authorization_header(
        self,authorization_header: str) -> str:
        """method to return Base64 athorization header.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """method to decode vlue of base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None
