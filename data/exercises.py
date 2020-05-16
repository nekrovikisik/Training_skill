import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

class Exercises(SqlAlchemyBase):
    __tablename__ = 'exercises'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    img_url = sqlalchemy.Column(sqlalchemy.String,
                              unique=True, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # workout1 = orm.relationship("Workout1")
    # workout2 = orm.relationship("Workout2")
    workouts = orm.relationship("Workouts")




