from db.base import database
from fastapi import FastAPI
from endpoints import users, auth, companies
from core.config import WEB_PORT, WEB_HOST
import uvicorn


app = FastAPI()
app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(companies.router, prefix='/companies', tags=['companies'])


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
    uvicorn.run("main:app", port=int(WEB_PORT), host=WEB_HOST, reload=True)
