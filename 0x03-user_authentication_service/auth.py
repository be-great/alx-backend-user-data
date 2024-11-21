#!/usr/bin/env python3
""" Authentication Module """

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> str:
    """hash password"""
    the_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return the_hash

# def _hash_password(password: str) -> str:
#     """ Returns a salted hash of the input password """
#     hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#     return hashed


def _generate_uuid() -> str:
    """Generate uuids"""
    uuid = uuid4()
    return str(uuid)

# def _generate_uuid() -> str:
#     """Returns a string representation of a new UUID"""
#     UUID = uuid4()
#     return str(UUID)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            thehash_pass = _hash_password(password)
            user = self._db.add_user(email, thehash_pass)
            return user

        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """check if the password valid or not"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        userPassword = user.hashed_password
        encodedPass = password.encode()
        if bcrypt.checkpw(encodedPass, userPassword):
            return True
        return False

    def create_session(self, email: str) -> str:
        """Get session id"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """take a session id and return a string or none"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """updates the user"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """generates a reset password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

#     def get_reset_password_token(self, email: str) -> str:
#         """Generates a reset password token if user exists"""
#         try:
#             user = self._db.find_user_by(email=email)
#         except NoResultFound:
#             raise ValueError

#         reset_token = _generate_uuid()

#         self._db.update_user(user.id, reset_token=reset_token)

#         return reset_token

#     def create_session(self, email: str) -> str:
#         """ Returns session ID for a user """
#         try:
#             user = self._db.find_user_by(email=email)
#         except NoResultFound:
#             return None

#         session_id = _generate_uuid()

#         self._db.update_user(user.id, session_id=session_id)

#         return session_id
# class Auth
#     def __init__(self):
#         self._db = DB()

#     def register_user(self, email: str, password: str) -> User:
#         """ Registers a user in the database
#         Returns: User Object
#         try:
#             user = self._db.find_user_by(email=email)
#         except NoResultFound:
#             hashed_password = _hash_password(password)
#             user = self._db.add_user(email, hashed_password)

#             return user

#         else:
#             raise ValueError(f'User {email} already exists')


#     def create_session(self, email: str) -> str:
#         """ Returns session ID for a user """
#         try:
#             user = self._db.find_user_by(email=email)
#         except NoResultFound:
#             return None

#         session_id = _generate_uuid()

#         self._db.update_user(user.id, session_id=session_id)

#         return session_id
#         try:
#             user = self._db.find_user_by(session_id=session_id)
#         except NoResultFound:
#             return None
#         return user
#     def destroy_session(self, user_id: int) -> None:
#         """Updates the corresponding user's session ID to None"""
#         try:
#             user = self._db.find_user_by(id=user_id)
#         except NoResultFound:
#             return None

#         self._db.update_user(user.id, session_id=None)

#         return None

#     def update_password(self, reset_token: str, password: str) -> None:
#         """Uses reset token to validate update of users password"""
#         if reset_token is None or password is None:
#             return None

#         try:
#             user = self._db.find_user_by(reset_token=reset_token)
#         except NoResultFound:
#             raise ValueError

#         hashed_password = _hash_password(password)
#         self._db.update_user(user.id,
#                              hashed_password=hashed_password,
#                              reset_token=None)
