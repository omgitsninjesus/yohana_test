# elevators.py
import asyncio
from typing import List
from fastapi import APIRouter, HTTPException, Path
from app.controller import controller
from app.api.models import ElevatorSchema, ElevatorDB
from app.api import crud
from app.config import ELEVATOR_COUNT, FLOOR_COUNT

router = APIRouter()


@router.get("/", status_code=200)
async def read_all_elevators():
    return await crud.get_all_elevators()


@router.get("/{id}/", status_code=200)
async def read_elevator(
    id: int = Path(..., gt=0),
):
    elevator = await crud.get_elevator(id)
    if not elevator:
        raise HTTPException(status_code=404, detail="Elevator not found")
    return elevator


@router.post("/", response_model=ElevatorDB, status_code=201)
async def create_elevator(payload: ElevatorSchema):
    elevator_id = await crud.post(payload)

    response_object = {
        "id": elevator_id,
        "floor": payload.floor,
    }
    return response_object


@router.put("/{id}/", status_code=201)
async def push_internal_button(
    payload: ElevatorSchema,
    id: int = Path(..., gt=0),
):
    elevator = await crud.get_elevator(id)
    if not elevator:
        raise HTTPException(status_code=404, detail="Elevator not found")

    await controller.push_internal(id, payload.floor)

    return {"status": "ok lets go"}
