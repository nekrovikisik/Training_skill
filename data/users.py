import datetime
import sqlalchemy
from sqlalchemy import orm, ForeignKey

from .db_session import SqlAlchemyBase


# from sqlalchemy_serializer import SerializerMixin

class Users(SqlAlchemyBase):
    __tablename__ = 'users'
    uid = sqlalchemy.Column(sqlalchemy.String, primary_key=True) #userid
    state = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=False)

    current_training = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    current_exercise = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    last_entrace = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, unique=False)
    last_training = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # хз будет ли связь с чем-то но мало ли
    #ex_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('exercises.id'))  # это айдишник конкретного упражнения

    # если че добавлю что-н


    # exercise = orm.relationship('Exercises')

    def __repr__(self):
        return '<Users> ' + str(self.uid) + ' ' + str(self.state) + ' ' + \
               str(self.last_entrace) + ' ' + str(self.last_training) + str(self.current_training) + ' ' + str(self.current_exercise)
