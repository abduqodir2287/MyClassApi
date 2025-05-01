from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from src.presentation.rest.routers import all_routers
from src.configs.logger_setup import logger
from src.presentation.rest.users.router import users_service


@asynccontextmanager
async def lifespan(my_app: FastAPI):
	await users_service.add_first_user()

	yield
	logger.info("Bye Bye !!!")


app = FastAPI(lifespan=lifespan)


for router in all_routers:
	app.include_router(router=router)


@app.get("/", status_code=status.HTTP_200_OK)
async def hello():
	return {"Message": "Hello World"}


