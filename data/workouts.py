import datetime
import sqlalchemy
from sqlalchemy import orm, ForeignKey

from .db_session import SqlAlchemyBase


# from sqlalchemy_serializer import SerializerMixin

class Workouts(SqlAlchemyBase):
    __tablename__ = 'workouts'
    i = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    num_id = sqlalchemy.Column(sqlalchemy.Integer,
                               unique=False)  # , primary_key=True) # это номер упражнения в конкретной тренеровке
    ex_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('exercises.id'))  # это айдишник конкретного упражнения
    # связь с exercises по этому ключу

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=False)  # название тренировки
    autor = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=False)  # айдишник автора тренировки

    rep = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, unique=False, default=20)
    rest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, unique=False,
                             default=120)  # время отдыха, по дефолту 120 секунд

    # ТЕСТ ТЕСТ ЕСЛИ ЧТО УДАЛИТЬ
    # exercise = orm.relationship('Exercises')

    def __repr__(self):
        return '<Workouts> ' + str(self.num_id) + ' ' + str(self.ex_id) + ' ' + \
               str(self.name) + ' ' + str(self.autor) + str(self.rep) + ' ' + str(self.rest)
