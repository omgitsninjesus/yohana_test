import asyncio
from fastapi import FastAPI
from app.api import ping, elevators, buttons
from app.db import engine, database, metadata
from app.api.crud import get_all_elevators
from app.controller import controller

metadata.create_all(engine)

app = FastAPI()

tasks = []


@app.on_event("startup")
async def startup():
    await database.connect()
    elevators = await get_all_elevators()
    controller.set_elevators(elevators)

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
