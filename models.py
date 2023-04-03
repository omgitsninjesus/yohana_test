# models.py


from datetime import datetime
from config import db, ma


class Elevator(db.Model):
    __tablename__ = "elevator"

    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class ElevatorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Elevator
        load_instance = True
        sqla_session = db.session


elevator_schema = ElevatorSchema()
building_schema = ElevatorSchema(many=True)
