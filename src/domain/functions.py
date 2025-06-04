from typing import Optional

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from src.configs.logger_setup import logger
from src.domain.enums import UserRole
from src.infrastructure.authentication.dependencies import check_user_role
from src.infrastructure.authentication.service import get_token


class ClassApiValidationFunctions:

    @staticmethod
    async def check_role_teacher_and_superadmin(token: str = Depends(get_token)) -> None:
        user_role = await check_user_role(token)
        allowed_roles = {UserRole.superadmin, UserRole.teacher}

        if user_role not in allowed_roles:
            logger.warning("Not enough rights!")

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights!")


    @staticmethod
    async def check_resource(resource: BaseModel, detail: Optional[str] = "Resource not found") -> None:
        
        if not resource:
            logger.info("Resource not found")

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


    @staticmethod
    async def check_password(password: str, real_password: str) -> None:

        if password != real_password:
            logger.warning("Wrong password")

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are writing the wrong password.")



