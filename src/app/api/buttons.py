# elevators.py
from typing import List
from fastapi import APIRouter, HTTPException, BackgroundTasks
import json

from app.api.models import BUTTONS
from app.api import crud
from app.config import FLOOR_COUNT
from app.controller import send_to_closest_elevator

router = APIRouter()


@router.get("/", status_code=200)
async def get_buttons():
    return BUTTONS


@router.post("/{id}/", status_code=201)
async def push_button(id: int):
    if 0 <= id < FLOOR_COUNT:
        button = BUTTONS[id]
        if button.pushed:
            raise HTTPException(
                status_code=400, detail=f"Button on floor {id} is already pushed"
            )
        button.push()
        elevator_id = await send_to_closest_elevator(id)
        return {"status": f"wait for elevator {elevator_id}"}
    else:
        raise HTTPException(
            status_code=404, detail=f"Button is not found on floor {id}"
        )
