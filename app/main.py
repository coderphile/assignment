from fastapi import FastAPI
from .database import engine
from .routes import address

app = FastAPI()

@app.on_event("startup")
async def startup_db():
    engine.connect()

@app.on_event("shutdown")
async def shutdown_db():
    engine.disconnect()

app.include_router(address.router, prefix="/addresses", tags=["addresses"])
