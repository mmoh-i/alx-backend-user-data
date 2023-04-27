#!/usr/bin/env python3
"""authentication module"""

from flask import request
import fnmatch
from typing import List, TypeVar
import os


class Auth():
    """
    Class to handle user authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method for require auth"""

        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        else:
            path = path.rstrip('/')
            for excluded_path in excluded_paths:
                excluded_path = excluded_path.rstrip('/')
                if fnmatch.fnmatch(path, excluded_path):
                    return False
            return True

    def authorization_header(self, request=None) -> str:
        """A method to authorize the header requests"""
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """current user method"""
        return None

    def session_cookie(self, request=None):
        """
        Method that returns a cookie value from a request
        """
        if request is None:
            return None
        user_cookies = os.getenv('SESSION_NAME')
        return request.cookies.get(user_cookies)
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Method to get the current user from a request.
        Args:
            request (flask.Request, optional): The Flask request object.
            Defaults to None.
        Returns:
            TypeVar('User'): The current user object.
        """
        return None
