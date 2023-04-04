import asyncio
from flask import abort, make_response

from config import FLOOR_COUNT

BUTTONS = [0] * FLOOR_COUNT


async def read_all():
    for _ in range(3):
        await asyncio.sleep(1)
        print("hi")


def read_one(id):
    if 0 <= id < FLOOR_COUNT:
        is_pushed = "" if BUTTONS[id] else "not "

        return make_response(f"Button {id} is {is_pushed}pushed", 200)
    else:
        abort(404, f"Button at floor {id} not found")
