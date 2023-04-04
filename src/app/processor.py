import asyncio


class ButtonProcessor:
    def __init__(self) -> None:
        self.queue = asyncio.Queue()

    async def push(self, floor: int):
        await self.queue.put(floor)

    async def process(self, name):
        while True:
            sleep_for = await self.queue.get()

            # Sleep for the "sleep_for" seconds.
            await asyncio.sleep(sleep_for)

            # Notify the queue that the "work item" has been processed.
            self.queue.task_done()

            print(f"{name} has slept for {sleep_for:.2f} seconds")





floor_button_processor = ButtonProcessor()


# @router.get("/start", response_model=List[ElevatorDB])
# async def start_elevators():
#     elevators = []
#     for i in range(ELEVATOR_COUNT):
#         elevator = asyncio.create_task(worker(f"elevator-{i}", floor_button_processor))
#         elevators.append(elevator)
