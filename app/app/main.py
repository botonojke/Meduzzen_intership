from fastapi import FastAPI
import databases

app = FastAPI()
DATABASE_URL = "postgresql://meduzzen_user:pass@db:5432/meduzzen_db"

database = databases.Database(DATABASE_URL)


@app.get('/')
async def status_root():
    return {"status": "Working"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
