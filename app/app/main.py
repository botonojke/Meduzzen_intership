from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def status_root():
    return {"status": "Working"}
