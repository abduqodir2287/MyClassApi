from fastapi import FastAPI, status

from src.presentation.rest.routers import all_routers


app = FastAPI()


for router in all_routers:
	app.include_router(router=router)



@app.get("/", status_code=status.HTTP_200_OK)
async def hello():
	return {"Message": "Hello World"}


