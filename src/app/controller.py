from typing import List
import asyncio
from app.api.models import ElevatorDB, BUTTONS, ElevatorStateSchema
from app.api.crud import elevator_update
from datetime import datetime
from time import mktime
from datetime import datetime

ELEVATOR_PACE_PER_FLOOR = 2  # seconds


class ElevatorController:
    PRIORITY_INTERNAL = 0
    PRIORITY_EXTERNAL = 1

    def __init__(self) -> None:
        self.queue = asyncio.PriorityQueue()
        self.elevators = {}

    def set_elevators(self, elevators: List[ElevatorDB]):
        self.elevators = {elevator.id: elevator for elevator in elevators}

    async def push_internal(self, elevator_id: int, floor: int) -> None:
        print(datetime.now(), f"User pushed {floor} inside elevator {elevator_id}")
        await self.queue.put((ElevatorController.PRIORITY_INTERNAL, floor, elevator_id))

    async def user_requested(self, elevator_id: int, floor: int) -> None:
        print(
            datetime.now(),
            f"External request from floor {floor} routed to elevator {elevator_id}",
        )
        await self.queue.put((ElevatorController.PRIORITY_EXTERNAL, floor, elevator_id))

    async def send_to_closest_elevator(self, floor: int) -> int:
        distances = [
            (elevator.id, abs(elevator.floor - floor))
            for elevator in self.elevators.values()
        ]
        distances.sort(key=lambda x: x[1])
        target_elevator_id = distances[0][0]
        print(f"sending request to elevator {target_elevator_id}")
        await self.user_requested(target_elevator_id, floor)
        return target_elevator_id

    async def run(self) -> None:
        while True:
            priority, desired_floor, elevator_id = await self.queue.get()
            print(f"Processing floor {desired_floor} for elevator {elevator_id}")
            elevator = self.elevators[elevator_id]
            print(elevator, elevator.moving)
            while elevator.moving:
                await asyncio.sleep(0.5)
            await self.move(elevator, desired_floor)
            self.queue.task_done()

    async def move(self, elevator: ElevatorDB, target_floor: int):
        floor_diff = target_floor - elevator.floor
        if floor_diff == 0:
            print(
                datetime.now(),
                f"Elevator {elevator.id} already on {target_floor} floor",
            )
            self.disable_button(target_floor)
            return

        payload = ElevatorStateSchema(floor=elevator.floor, moving=True)
        await elevator_update(elevator.id, payload)
        print("done")
        direction = 1 if target_floor > elevator.floor else -1  # 1 for up, -1 for down
        await asyncio.sleep(ELEVATOR_PACE_PER_FLOOR)

        for floor in range(elevator.floor + direction, target_floor, direction):
            print(datetime.now(), f"Elevator {elevator.id} passing floor {floor}")
            payload.floor = floor
            await elevator_update(elevator.id, payload)
            await asyncio.sleep(ELEVATOR_PACE_PER_FLOOR)

        print(datetime.now(), f"Elevator {elevator.id} arrived on floor {target_floor}")

        payload.floor = floor
        payload.moving = False
        await elevator_update(elevator.id, payload)

        self.disable_button(target_floor)

    def disable_button(self, floor: int):
        BUTTONS[floor].light_off()


controller = ElevatorController()
