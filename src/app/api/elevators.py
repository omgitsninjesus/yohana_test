# elevators.py
import asyncio
from typing import List
from fastapi import APIRouter, HTTPException, Path

from app.api.models import ElevatorSchema, ELEVATORS, CONTROLLERS
from app.api import crud
from app.config import ELEVATOR_COUNT, FLOOR_COUNT

router = APIRouter()

TURNED_ON = False


@router.get("/", status_code=200)
async def read_all_elevators():
    return ELEVATORS


@router.get("/{id}/", status_code=200)
async def read_elevator(
    id: int = Path(..., ge=0, lt=ELEVATOR_COUNT),
):
    elevator = ELEVATORS[id]
    if not elevator:
        raise HTTPException(status_code=404, detail="Elevator not found")
    return elevator


# @router.post("/", response_model=ElevatorDB, status_code=201)
# async def create_elevator(payload: ElevatorSchema):
#     elevator_id = await crud.post(payload)

#     response_object = {
#         "id": elevator_id,
#         "floor": payload.floor,
#     }
#     return response_object


@router.put("/{id}/", status_code=201)
async def push_internal_button(
    payload: ElevatorSchema,
    id: int = Path(..., ge=0, lt=ELEVATOR_COUNT),
):
    controller = CONTROLLERS[id]

    await controller.push_internal(payload.floor)

    return {"status": "ok lets go"}


# @router.post("/", response_model=ElevatorDB, status_code=201)
# async def create_note(payload: ElevatorSchema):
#     note_id = await crud.post(payload)

#     response_object = {
#         "id": note_id,
#         "title": payload.title,
#         "description": payload.description,
#     }
#     return response_object


# from flask import abort
# from config import db
# from models import Elevator, building_schema, elevator_schema


# def read_all():
#     elevators = Elevator.query.all()
#     return building_schema.dump(elevators)


# def read_one(id):
#     elevator = Elevator.query.filter(Elevator.id == id).one_or_none()
#     if elevator is not None:
#         return elevator_schema.dump(elevator)
#     else:
#         abort(404, f"Elevator with id {id} not found")


# def update(id, elevator):
#     existing_elevator = Elevator.query.filter(Elevator.id == id).one_or_none()
#     if existing_elevator:
#         update_elevator = elevator_schema.load(elevator, session=db.session)
#         existing_elevator.floor = update_elevator.floor
#         db.session.merge(existing_elevator)
#         db.session.commit()
#         return elevator_schema.dump(existing_elevator), 201

#     else:
#         abort(404, f"Elevator with id {id} not found")
