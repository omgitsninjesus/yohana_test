# models.py
import asyncio

from pydantic import BaseModel, Field
from app.config import FLOOR_COUNT, ELEVATOR_COUNT
from datetime import datetime
from time import mktime

ELEVATOR_PACE_PER_FLOOR = 2  # seconds


class ElevatorSchema(BaseModel):
    floor: int = Field(..., ge=0, lt=FLOOR_COUNT)


class ButtonSchema(BaseModel):
    floor: int


class Elevator:
    def __init__(self, id: int, floor: int = Field(..., ge=0, lt=FLOOR_COUNT)):
        self.id = id
        self.floor = floor
        self.moving = False
        self.doors_opened = False  # TODO don't move with doors opened
        self.last_movement = mktime(datetime.now().timetuple())

    async def move(self, target_floor: int):

        floor_diff = target_floor - self.floor
        if floor_diff == 0:
            print(datetime.now(), f"Elevator {self.id} already on {target_floor} floor")
            self.disable_button(target_floor)
            return

        self.moving = True
        direction = 1 if target_floor > self.floor else -1  # 1 for up, -1 for down
        await asyncio.sleep(ELEVATOR_PACE_PER_FLOOR)

        for floor in range(self.floor + direction, target_floor, direction):
            print(datetime.now(), f"Elevator {self.id} passing floor {floor}")
            self.floor = floor
            await asyncio.sleep(ELEVATOR_PACE_PER_FLOOR)

        print(datetime.now(), f"Elevator {self.id} arrived on floor {target_floor}")
        self.floor = target_floor
        self.disable_button(target_floor)
        self.last_movement = mktime(datetime.now().timetuple())
        self.moving = False

    def disable_button(self, floor: int):
        BUTTONS[floor].light_off()


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


ELEVATORS = [Elevator(i, 1) for i in range(ELEVATOR_COUNT)]
BUTTONS = [FloorButton(i) for i in range(FLOOR_COUNT)]
