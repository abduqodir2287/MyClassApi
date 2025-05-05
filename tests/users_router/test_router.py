import pytest
from fastapi import status

from src.domain.users.schema import UsersModelForGet

@pytest.mark.asyncio
async def test_get_all_users_page(async_client) -> None:
    response = await async_client.get("/Users")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    users = [UsersModelForGet(**item) for item in data]
    print(users)

    assert users

