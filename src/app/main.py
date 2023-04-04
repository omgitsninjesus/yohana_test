import asyncio
from fastapi import FastAPI
from app.api import ping, elevators, buttons
from app.db import engine, database, metadata
from app.controller import CONTROLLERS

metadata.create_all(engine)

app = FastAPI()

tasks = []


@app.on_event("startup")
async def startup():
    await database.connect()
    for controller in CONTROLLERS:
        task = asyncio.create_task(controller.run())
        tasks.append(task)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    for task in tasks:
        task.cancel()


app.include_router(ping.router)
app.include_router(elevators.router, prefix="/elevators", tags=["elevators"])
app.include_router(buttons.router, prefix="/buttons", tags=["buttons"])
