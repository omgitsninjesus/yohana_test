import asyncio
from app.api.models import Elevator, ELEVATORS, ELEVATOR_COUNT
from datetime import datetime


class ElevatorController:
    PRIORITY_INTERNAL = 0
    PRIORITY_EXTERNAL = 1

    def __init__(self, elevator: Elevator) -> None:
        self.queue = asyncio.PriorityQueue()
        self.elevator = elevator

    async def push_internal(self, floor: int) -> None:
        print(datetime.now(), f"User pushed {floor} inside elevator {self.elevator.id}")
        await self.queue.put((ElevatorController.PRIORITY_INTERNAL, floor))

    async def user_requested(self, floor: int) -> None:
        print(
            datetime.now(),
            f"External request from floor {floor} routed to elevator {self.elevator.id}",
        )
        await self.queue.put((ElevatorController.PRIORITY_EXTERNAL, floor))

    async def run(self) -> None:
        while True:
            _, desires_floor = await self.queue.get()
            print("Processing", desires_floor)
            while self.elevator.moving:
                await asyncio.sleep(0.1)
            await self.elevator.move(desires_floor)
            self.queue.task_done()


CONTROLLERS = [ElevatorController(ELEVATORS[i]) for i in range(ELEVATOR_COUNT)]


async def send_to_closest_elevator(floor: int) -> Elevator:
    distances = [(cntrl, abs(cntrl.elevator.floor - floor)) for cntrl in CONTROLLERS]
    distances.sort(key=lambda x: x[1])
    controller = distances[0][0]
    print(f"sending request to elevator {controller.elevator.id}")
    await controller.user_requested(floor)
    return controller.elevator.id
