from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
	POSTGRES_DB: str = None
	POSTGRES_HOST: str = None
	POSTGRES_PORT: int = None
	POSTGRES_USER: str = None
	POSTGRES_PASSWORD: str = None
	SECRET_KEY: str = None
	ALGORITHM: str = None
	APPLICATION_PORT: int = None
	APPLICATION_HOST: str = None
	DOCKER_EXPOSED_PORT: int = None
	LOG_LEVEL: str = None
	LOG_FORMAT: str = None
	LOG_FILE: str = None
	LOG_BACKUP_COUNT: int = None
	LOG_WRITE_STATUS: bool = None


	@property
	def DATABASE_URL(self) -> str:
		return f"postgresql+asyncpg://{self.POSTGRES_USER}:" \
		       f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"


	@property
	def GET_AUTH_DATA(self) -> dict:
		return {"secret_key": self.SECRET_KEY, "algorithm": self.ALGORITHM}



	model_config = SettingsConfigDict(env_file=".env")



@lru_cache()
def get_settings():
	return Settings()

