from pydantic import BaseModel, Field, model_validator
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime

from src.configs.logger_setup import logger


class Date(BaseModel):
	date: Optional[str] = Field(
		None, description="The person's date of birth in the format 'DD-MM-YYYY'.",
		examples=["01-01-2007"]
	)

	@model_validator(mode="before")
	def validate_birth_date(cls, values):
		date = values.get("date")

		try:
			if isinstance(date, str) and len(date) == 10:
				datetime.strptime(date, "%d-%m-%Y")

				return values

		except ValueError as e:
			logger.warning(f"{e}")

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		                    detail="Write the correct birthday. The date must be in the format 'DD-MM-YYYY'.")


