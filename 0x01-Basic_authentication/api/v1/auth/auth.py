#!/usr/bin/env python3
"""authentication module"""

from flask import request
import fnmatch
from typing import List, TypeVar


class Auth():
    """
    Class to handle user authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method for require auth"""

        # unaccepted_path = f"{path}/"
        # if path is None:
        #     return True
        # elif excluded_paths is None or excluded_paths == []:
        #     return True
        # elif path in excluded_paths or unaccepted_path in excluded_paths:
        #     return False
        # return True

        # Modification for final task 101
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
