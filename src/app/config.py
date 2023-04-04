# config.py

import pathlib

FLOOR_COUNT = 5
ELEVATOR_COUNT = 2

basedir = pathlib.Path(__file__).parent.resolve()
db_url = f"sqlite:///{basedir / 'elevators.db'}"
