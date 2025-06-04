from contextlib import nullcontext
import pytest
from httpx import AsyncClient
from fastapi import status



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_model, expectation",
    [
        ({"username": "anvar", "password": "90 yilla"}, nullcontext())
        # ({"username": "abduqodir", "password": "09"}, pytest.raises(ValidationError))
    ]
)
async def test_add_users(client: AsyncClient, user_model, expectation) -> None:
    with expectation:
        response = await client.post(url="/Users/add_user", json=user_model)

        assert response.status_code == status.HTTP_201_CREATED
        assert "Result" in response.json()


@pytest.mark.asyncio
async def test_add_users(client: AsyncClient, prepare_test_db) -> None:
    response = await client.get(url="/Users")

    assert response.status_code == status.HTTP_200_OK
    print(response.json())

