import os

from databases import Database
from app.config import db_url, ELEVATOR_COUNT, FLOOR_COUNT
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    Boolean,
)
from sqlalchemy.sql import func
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", db_url)

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

elevators = Table(
    "elevators",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("floor", Integer),
    Column(
        "last_movement",
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
    Column("moving", Boolean, default=False),
    # TODO: better not move with doors opened. Not used.
    Column("doors_opened", Boolean, default=False),
)

buttons = Table(
    "buttons",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("floor", Integer),
    Column("pushed", Boolean),
    Column(
        "pushed_since",
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    ),
)


# databases query builder
database = Database(DATABASE_URL)
