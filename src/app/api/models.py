# models.py
import asyncio

from pydantic import BaseModel, Field
from app.config import FLOOR_COUNT, ELEVATOR_COUNT
from datetime import datetime
from time import mktime


class ElevatorSchema(BaseModel):
    floor: int = Field(..., ge=0, lt=FLOOR_COUNT)


class ElevatorStateSchema(BaseModel):
    floor: int = Field(..., ge=0, lt=FLOOR_COUNT)
    moving: bool


class ElevatorDB(ElevatorSchema):
    id: int
    moving: bool


# not used
class ButtonSchema(BaseModel):
    floor: int


class FloorButton:
    def __init__(self, floor: int) -> None:
        self.floor = floor
        self.pushed = False
        self.ts_pushed = mktime(datetime.now().timetuple())

    def push(self):
        self.pushed = True
        self.ts_pushed = mktime(datetime.now().timetuple())

    def light_off(self):
        self.pushed = False


BUTTONS = [FloorButton(i) for i in range(FLOOR_COUNT)]
