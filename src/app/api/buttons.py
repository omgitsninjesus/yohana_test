# elevators.py
from typing import List
from fastapi import APIRouter, HTTPException
import json

from app.api.models import BUTTONS, send_to_closest_elevator
from app.api import crud
from app.config import FLOOR_COUNT
from app.processor import floor_button_processor

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
        button.pushed = True
        await send_to_closest_elevator(id)
        return {"status": "wait"}
    else:
        raise HTTPException(
            status_code=404, detail=f"Button is not found on floor {id}"
        )
