from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request, Depends, status

from src.configs.config import settings
from src.configs.logger_setup import logger


def create_access_token(data: dict) -> str:
	to_encode = data.copy()

	expire = datetime.now(timezone.utc) + timedelta(days=1)
	to_encode.update({"expire": int(expire.timestamp())})
	auth_data = settings.GET_AUTH_DATA

	encoded_token = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])

	return encoded_token


def get_token(request: Request) -> str | None:
	access_token = request.cookies.get("user_access_token")

	if not access_token:
		logger.warning("Token not found")
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized")

	return access_token


def decode_access_token(token: str = Depends(get_token)) -> dict | None:
	try:
		auth_data = settings.GET_AUTH_DATA
		payload = jwt.decode(token, auth_data["secret_key"], algorithms=auth_data["algorithm"])
	except JWTError:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token!")

	return payload
