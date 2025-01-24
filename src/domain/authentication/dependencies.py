from fastapi import Depends, HTTPException, status
from datetime import datetime, timezone

from src.domain.authentication.auth import decode_access_token, get_token
from src.domain.enums import UserRole
from src.infrastructure.database.postgres.users.client import UsersTable

users_table = UsersTable()


async def check_user_role(token: str = Depends(get_token)) -> UserRole:
	payload = decode_access_token(token)

	expire = payload.get("expire")
	if not expire:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

	expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
	if expire_time < datetime.now(timezone.utc):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')

	user_id = int(payload.get("sub"))
	user_by_id = await users_table.select_users(user_id=user_id)

	if user_by_id:
		return user_by_id.role

	raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something went wrong. Go fuck yourself')




