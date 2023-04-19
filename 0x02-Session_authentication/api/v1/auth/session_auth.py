#!/usr/bin/env python3
"""Session authentication module"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Session authentication class that inherits from Auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """method to create session id so as to
        to be able to retrieve user_id based on session
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        A class method that returns a User ID based on a Session ID
        """
        if session_id is None or type(session_id) is not str:
            return None
        value = self.user_id_by_session_id.get(session_id)
        return value

    def current_user(self, request=None):
        """
        (overload) that returns a User instance
        based on a cookie value:
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None) -> bool:
        """A method that deletes the user session / logout:"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
