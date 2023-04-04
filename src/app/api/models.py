# models.py
import asyncio

from pydantic import BaseModel, Field
from app.config import FLOOR_COUNT, ELEVATOR_COUNT


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

    async def move(self, target_floor: int):

        floor_diff = target_floor - self.floor
        if floor_diff == 0:
            print(f"Elevator {self.id} already on {target_floor} floor")
            self.disable_button(target_floor)
            return

        self.moving = True
        upward_dir = 1 if target_floor > self.floor else -1
        await asyncio.sleep(1)

        for floor in range(self.floor + upward_dir, target_floor, upward_dir):
            print(f"Elevator {self.id} passing floor {floor}")
            self.floor = floor
            await asyncio.sleep(1)

        print(f"Elevator {self.id} arrived on floor {target_floor}")
        self.floor = target_floor
        self.disable_button(target_floor)
        self.moving = False

    def disable_button(self, floor: int):
        BUTTONS[floor].pushed = False


class ElevatorController:
    PRIORITY_INTERNAL = 0
    PRIORITY_EXTERNAL = 1

    def __init__(self, elevator: Elevator) -> None:
        self.queue = asyncio.PriorityQueue()
        self.elevator = elevator

    async def push_internal(self, floor: int) -> None:
        print(f"User pushed {floor} inside elevator {self.elevator.id}")
        await self.queue.put((ElevatorController.PRIORITY_INTERNAL, floor))

    async def user_requested(self, floor: int) -> None:
        print(
            f"External request from floor {floor} routed to elevator {self.elevator.id}"
        )
        await self.queue.put((ElevatorController.PRIORITY_EXTERNAL, floor))

    async def process_input(self) -> None:
        while True:
            priority, desires_floor = await self.queue.get()
            print("Processing", desires_floor)
            while self.elevator.moving:
                await asyncio.sleep(0.1)
            await self.elevator.move(desires_floor)
            self.queue.task_done()


class FloorButton:
    def __init__(self, floor: int) -> None:
        self.floor = floor
        self.pushed = False


ELEVATORS = [Elevator(i, 1) for i in range(ELEVATOR_COUNT)]
BUTTONS = [FloorButton(i) for i in range(FLOOR_COUNT)]
CONTROLLERS = [ElevatorController(ELEVATORS[i]) for i in range(ELEVATOR_COUNT)]


async def send_to_closest_elevator(floor: int) -> Elevator:
    distances = [(cntrl, abs(cntrl.elevator.floor - floor)) for cntrl in CONTROLLERS]
    distances.sort(key=lambda x: x[1])
    controller = distances[0][0]
    print(f"sending request to elevator {controller.elevator.id}")
    await controller.user_requested(floor)
