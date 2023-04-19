#!/usr/bin/env python3
"""The basic authentication module"""

from api.v1.auth.auth import Auth
from typing import TypeVar, Tuple
from models.user import User
import base64


class BasicAuth(Auth):
    """Basic Authentication class that inherits from Auth"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        returns the Base64 part of the
        Authorization header for a Basic Authentication:
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        A method that returns the decoded value of Base64
        string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            auth_token = base64.b64decode(base64_authorization_header)
            return auth_token.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """
        A method that returns the user email and
        password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        # modified for task 12
        user_info = decoded_base64_authorization_header.partition(":")
        email = user_info[0]
        password = user_info[2]

        return email, password

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """
        A method that that returns the User instance based on his
        email and password.
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        users = User().search({"email": user_email})
        if not users or users == []:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request:
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        enc_b64_header = self.extract_base64_authorization_header(auth_header)
        if enc_b64_header is None:
            return None
        de_b64_header = self.decode_base64_authorization_header(enc_b64_header)
        if de_b64_header is None:
            return None
        user_cred = self.extract_user_credentials(de_b64_header)
        if user_cred is None:
            return None
        user = self.user_object_from_credentials(user_cred[0], user_cred[1])
        return user
