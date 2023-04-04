from app.api.models import ElevatorSchema, ElevatorStateSchema
from app.db import elevators, database, buttons


async def get_all_elevators():
    query = elevators.select()
    return await database.fetch_all(query=query)


async def get_elevator(id: int):
    query = elevators.select().where(id == elevators.c.id)
    return await database.fetch_one(query=query)


async def post(payload: ElevatorSchema):
    query = elevators.insert().values(floor=payload.floor)
    return await database.execute(query=query)


async def elevator_update(id: int, payload: ElevatorStateSchema):
    query = (
        elevators.update()
        .where(id == elevators.c.id)
        .values(floor=payload.floor, moving=payload.moving)
        .returning(elevators.c.id)
    )
    return await database.execute(query=query)


async def get_button(id: int):
    query = buttons.select().where(id == buttons.c.id)
    return await database.fetch_one(query=query)
