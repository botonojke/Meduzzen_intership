from fastapi import FastAPI
from db.credentials import database

app = FastAPI()


@app.get('/')
async def status_root():
    return {"status": "Working"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
