import pytest
from contextlib import nullcontext
from pydantic import BaseModel
from pydantic_core._pydantic_core import ValidationError
from fastapi import HTTPException

from src.domain.functions import ClassApiValidationFunctions
from src.domain.schema import ResponseForPost


class TestApiValidator:

    def setup_method(self):
        self.validator = ClassApiValidationFunctions()


    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "resource_data, detail, expectation",
        [
            ({"Status": "Created", "ID": 25}, "User not found", nullcontext()),
            ({"ID": 25}, None, nullcontext()),
            ({"Status": "Created", "ID": "asd"}, None, pytest.raises(ValidationError)),
        ]
    )
    async def test_check_resource(self, resource_data: dict, detail: str, expectation) -> None:
        with expectation:
            resource: BaseModel = ResponseForPost(**resource_data)
            await self.validator.check_resource(resource, detail)


    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "password, real_password, expectation",
        [("04042000", "04042000", nullcontext()), ("04042000", "582#post", pytest.raises(HTTPException))]
    )
    async def test_check_password(self, password: str, real_password: str, expectation) -> None:
        with expectation:
            await self.validator.check_password(password, real_password)


