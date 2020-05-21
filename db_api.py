from my_api import *
from data import db_session
from data.exercises import Exercises
from data.workouts import Workouts
from data.users import Users
from data.db_session import SqlAlchemyBase

def is_new_user(session, req):
    # uid = setUserId(req)
    uid = user_id(req)
    return not (session.query(Users.uid).filter(Users.uid == uid).first())

def getLast_entrace(session,user_id):
    day = session.query(Users.last_entrace).filter(Users.uid == user_id).first()[0]
    return day

def getWorkouts(session, autor='vikisik'):
    all_w = session.query(Workouts.name).filter(Workouts.ex_id == Exercises.id, Workouts.autor == autor).all()
    all_w = sorted(list(set(all_w)))
    return [i[0].lower() for i in all_w]

def getExercises_list(session, autor, workout_name):
    return session.query(Workouts.num_id, Exercises.name, Workouts.ex_id, Exercises.about, Workouts.rep,
                  Workouts.rest).filter(
        Workouts.name == workout_name, Workouts.ex_id == Exercises.id,
        Workouts.autor == autor).all()

def getWorkout_names(session, autor):
    all_w = session.query(Workouts.name).filter(Workouts.ex_id == Exercises.id, Workouts.autor == autor).all()
    all_w = sorted(list(set(all_w)))
    return [i[0].lower() for i in all_w]
