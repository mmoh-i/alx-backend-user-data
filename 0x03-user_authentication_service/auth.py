#!/usr/bin/env python3
"""Authentication module"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hashes the password and returns bytes"""
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid() -> str:
    """Generates a str uuid4"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new user to the database"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            passwd = _hash_password(password).decode('utf-8')
            return self._db.add_user(email=email, hashed_password=passwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Validates the credential for user login"""
        try:
            user = self._db.find_user_by(email=email)
            passwd = password.encode('utf-8')
            user_passwd = user.hashed_password.encode('utf-8')
            return bcrypt.checkpw(passwd, user_passwd)

        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Creates a user session"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Finds and gets user by session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys user session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset token for the user"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Method to update the password of the user"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            passwd = _hash_password(password).decode('utf-8')
            self._db.update_user(
                user.id,
                hashed_password=passwd,
                reset_token=None
            )

        except NoResultFound:
            raise ValueError
