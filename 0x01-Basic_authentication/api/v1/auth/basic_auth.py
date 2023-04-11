#!/usr/bin/env python3
"""Basic authentication module
to inherit from auth
"""
from flask import request
from typing import List, TypeVar
import base64


class BasicAuth(Auth):
  def extract_base64_authorization_header(self, authorization_header: str) -> str:
    """method to return Base64 athorization header.
    """
    if authorization_header is None or not isinstance(authorization_header, str):
            return None
        
        if not authorization_header.startswith('Basic '):
            return None
        
        return authorization_header.split(' ')[1]
