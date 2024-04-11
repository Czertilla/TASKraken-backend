import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, models, exceptions
from fastapi_users.jwt import generate_jwt, decode_jwt
import jwt  

from repositories.users import  get_user_db
from models.users import UserORM
from utils.settings import getSettings
from logging import getLogger

SECRET = getSettings().PASSW_SECTRET

logger = getLogger(__name__)

class UserManager(UUIDIDMixin, BaseUserManager[UserORM, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserORM, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserORM, token: str, request: Optional[Request] = None
    ):
        logger.warning(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: UserORM, token: str, request: Optional[Request] = None
    ):
        logger.warning(f"Verification requested for user {user.id}. Verification token: {token}")
    
    async def request_verify(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        if not user.is_active:
            raise exceptions.UserInactive()
        if user.is_verified:
            raise exceptions.UserAlreadyVerified()

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.verification_token_secret,
            self.verification_token_lifetime_seconds,
        )
        await self.on_after_request_verify(user, token, request)

    async def verify(self, token: str, request: Optional[Request] = None) -> models.UP:
        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
        except jwt.PyJWTError:
            raise exceptions.InvalidVerifyToken()

        try:
            user_id = data["sub"]
            email = data["email"]
        except KeyError:
            raise exceptions.InvalidVerifyToken()

        try:
            user = await self.get_by_email(email)
        except exceptions.UserNotExists:
            raise exceptions.InvalidVerifyToken()

        try:
            parsed_id = self.parse_id(user_id)
        except exceptions.InvalidID:
            raise exceptions.InvalidVerifyToken()

        if parsed_id != user.id:
            raise exceptions.InvalidVerifyToken()

        if user.is_verified:
            raise exceptions.UserAlreadyVerified()

        verified_user = await self._update(
            user, 
            {
                "is_verified": True,
                "role": "specialist"
            }
        )

        await self.on_after_verify(verified_user, request)

        return verified_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)