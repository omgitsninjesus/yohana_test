from app.api.models import ElevatorSchema
from app.db import elevators, database, buttons


async def get_all():
    query = elevators.select()
    return await database.fetch_all(query=query)


async def get(id: int):
    query = elevators.select().where(id == elevators.c.id)
    return await database.fetch_one(query=query)


async def post(payload: ElevatorSchema):
    query = elevators.insert().values(floor=payload.floor)
    return await database.execute(query=query)


async def get_button(id: int):
    query = buttons.select().where(id == buttons.c.id)
    return await database.fetch_one(query=query)
