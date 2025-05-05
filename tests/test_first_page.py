import pytest
from fastapi import status



@pytest.mark.asyncio
async def test_first_page(async_client) -> None:
    response = await async_client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Message": "Hello World"}
