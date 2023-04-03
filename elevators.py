# elevators.py

from flask import abort
from config import db
from models import Elevator, building_schema, elevator_schema


def read_all():
    elevators = Elevator.query.all()
    return building_schema.dump(elevators)


def read_one(id):
    elevator = Elevator.query.filter(Elevator.id == id).one_or_none()
    if elevator is not None:
        return elevator_schema.dump(elevator)
    else:
        abort(404, f"Elevator with id {id} not found")


def update(id, elevator):
    existing_elevator = Elevator.query.filter(Elevator.id == id).one_or_none()
    if existing_elevator:
        update_elevator = elevator_schema.load(elevator, session=db.session)
        existing_elevator.floor = update_elevator.floor
        db.session.merge(existing_elevator)
        db.session.commit()
        return elevator_schema.dump(existing_elevator), 201

    else:
        abort(404, f"Elevator with id {id} not found")
