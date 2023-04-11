#!/usr/bin/env python3
"""
This module contains the implementation of the Auth class,
which is used to manage API authentication.
The Auth class is the template for all
authentication systems to be implemented. It provides three methods:
- require_auth: to require authentication for a path
- authorization_header: to get the authorization header from a request
- current_user: to get the current user from a request
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Class to manage API authentication.
    This class is the template for all
    authentication systems to be implemented.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to require authentication for a path.
        Args:
            path (str): The path to require authentication for.
            excluded_paths (List[str]): A list of paths that are excluded
            from authentication.
        Returns:
            bool: Whether or not authentication is required.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                if excluded_path.endswith('/'):
                    return False
                elif path.endswith('/') == excluded_path[:-1]:
                    return False
                elif path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Method to get the authorization header from a request.
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Method to get the current user from a request.
        Args:
            request (flask.Request, optional): The Flask request object.
            Defaults to None.
        Returns:
            TypeVar('User'): The current user object.
        """
        return None
