#!/usr/bin/env python3
""" Session expiration module """

from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """
    session exp class i.e handles the expiration of a session
    """
    def __init__(self) -> None:
        """initializes the class instance"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Overloads the create session and returns the session id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a user_id based on a session id
        by overloading user_id_for_session
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_info = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_info.get('user_id')

        if session_info.get('created_at') is None:
            return None

        created_at = session_info.get('created_at')
        duration = created_at + timedelta(seconds=self.session_duration)

        if duration < datetime.now():
            return None
        return session_info.get('user_id')
