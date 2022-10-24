from db.base import database
from fastapi import FastAPI
from endpoints import users
import uvicorn


app = FastAPI()
app.include_router(users.router, prefix='/users', tags=['users'])


@app.get('/')
async def status_root():
    return {"status": "Working"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
