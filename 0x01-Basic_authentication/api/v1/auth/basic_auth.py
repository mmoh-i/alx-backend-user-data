#!/usr/bin/env python3
"""Basic authentication module
to inherit from auth
"""
from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """
    Class that implements Basic Authentication.
    Inherits from Auth.
    """
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """method to return Base64 athorization header.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """method to decode vlue of base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header
            ).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """eturns the user email and password
        from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        user_info = decoded_base64_authorization_header.partition(":")
        email = user_info[0]
        password = user_info[2]
        return email, password

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """returns the User instance based on
        email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User().search({"email": user_email})
        if not users or users == []:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves
        the User instance for a request"""
        if request is None:
            return None
        auth_header = self.authorization_header(reuques)
        if auth_header is None:
            return None

        encoded_credentials = self.extract_base64_authorization_header(
            auth_header)
        if encoded_credentils is None:
            return None
        decoded_credentials = self.decode_base64_authorization_header(
            encoded_credentials)
        if decoded_credentials is None:
            return None
        email, pwd = self.extract_user_credentials(decoded_credentials)
        user = self.user_object_from_credentials(email, pwd)
        return user
