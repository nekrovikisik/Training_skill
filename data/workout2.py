import datetime
import sqlalchemy
from sqlalchemy import orm, ForeignKey

from .db_session import SqlAlchemyBase


# from sqlalchemy_serializer import SerializerMixin

class Workout2(SqlAlchemyBase):
    __tablename__ = 'workout2'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    ex_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('exercises.id'))
    # тут айдишник упражненияключу
    # # связь с exercises по этому ключу

    rep = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, unique=False, default=20)
    rest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, unique=False,
                              default=120) # время отдыха, по дефолту 120 секунд
    # ТЕСТ ТЕСТ ЕСЛИ ЧТО УДАЛИТЬ
   # exercise = orm.relationship('Exercises')

    def __repr__(self):
        return '<Workout Two> ' + str(self.id) + ' '  + str(self.ex_id) + ' ' + str(self.rep) + ' ' + str(self.rest)
