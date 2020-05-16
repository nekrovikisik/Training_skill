from flask import Flask
from data import db_session
from data.exercises import Exercises
from data.workout2 import Workout2
from data.workout1 import Workout1
from data.db_session import SqlAlchemyBase
import random

db_session.global_init("/home/victoria/PycharmProjects/lyceumTest/WEB_YL/Training_skill/db/Exercises.sqlite")
session = db_session.create_session()

def fill_table():
    for i in range(1, 21):
        exercise = Exercises()
        exercise.id = i
        exercise.name = 'упражнение ' + str(i)
        exercise.about = "выполнять с чувством, с тактом "+ str(i)
        exercise.img_url = 'my_url' + str(i)

        session.add(exercise)
        session.commit()

    for i in range(1, 8):
        workout1 = Workout1()#, exercise='упражнение ' + str(i))
        workout2 = Workout2()#, exercise='упражнение ' + str(i))
        workout1.ex_id = random.choice(range(1, 21))
        workout2.ex_id = random.choice(range(1, 21))
        workout1.id = i
        workout2.id = i
        session.add(workout1)
        session.add(workout2)
        session.commit()
    my_workout = session.query(Workout2).filter_by(id=1).first()
    print(my_workout)


def getExercises(workout_num): # на выходе словарь тренировки
    # INPUT: объект класса тренировки
    # OUTPUT: {'id': [номера упраж из Exercises], 'name': [названия упраж],'about': [доп. инфа]}

    exercises_list = session.query(workout_num.ex_id, Exercises.name, Exercises.about).filter(
        workout_num.ex_id == Exercises.id).all()
    my_keys = exercises_list[0]._asdict().keys()
    exerc_dict = {key: [exercises_list[0]._asdict()[key]] for key in my_keys}
    for workout in exercises_list[1:]:
        workout = workout._asdict()
        for key in exerc_dict.keys():
            exerc_dict[key].append(workout[key])
    return exerc_dict

fill_table()
print(getExercises(Workout2))