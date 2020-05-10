'''ТУТ ШПАРГАЛКА
        https://lyceum.yandex.ru/courses/166/groups/1337/lessons/1721/materials/4044#4

'''
import random

from flask import Flask, request
from data import db_session
import logging
import json
from flask import Flask
from data import db_session
from data.exercises import Exercises
from data.workout2 import Workout2
from data.workout1 import Workout1
from data.db_session import SqlAlchemyBase
import random

app = Flask(__name__)
logging.basicConfig(level=logging.INFO) # уровень логирования

sessionStorage = {}
# для каждой сессии общения хранятся подсказки, которые видел пользователь.
# (buttons в JSON ответа).
CHOOSE = {'random': ['случайная', 'рандом', 'все равно' , 'своя', 'собственная', 'моя'] }
WORKOUTS = {'Тренировка один': Workout1, 'Тренировка два': Workout2}
session = db_session.create_session()
db_session.global_init("db/Exercises.sqlite")


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

def getExercises(workout_num): # на выходе словарь тренировки
    # INPUT: объект класса тренировки
    # OUTPUT: {'id': [номера упраж из Exercises], 'name': [названия упраж],
    # 'about': [доп. инфа],'rep': [число повторений], 'rest': [отдых в секундах]}

    exercises_list = session.query(workout_num.ex_id, Exercises.name,
                        Exercises.about, workout_num.rep, workout_num.rest)\
                        .filter(workout_num.ex_id == Exercises.id).all()

    my_keys = exercises_list[0]._asdict().keys()
    exerc_dict = {key: [exercises_list[0]._asdict()[key]] for key in my_keys}
    for workout in exercises_list[1:]:
        print(workout)
        workout = workout._asdict()
        for key in exerc_dict.keys():
            exerc_dict[key].append(workout[key])
    return exerc_dict



def base_workouts(req, res):
    workout_name = random.choose(WORKOUTS.keys())
    my_workout = getExercises(workout_name)
    sessionStorage['workout_name'] = workout_name
    num_ex = len(my_workout['name']) # число упражнений в тренировке
    ex_list = ''
    for i in range(1, num_ex + 1):
        ex_list.append(F"{str(i)}. {my_workout['name']}, "
                       F"{my_workout['rep']} повторений, {my_workout['rest']} секунд отдыха.")
    res['response']['text'] = '\n'.join((ex_list))

def handle_dialog(req, res):
    if not sessionStorage['is_started']:
        start(req, res)
    else:
        if req['request']['original_utterance'].lower() in CHOOSE['random']:
            base_workouts(req, res)
        if req['request']['original_utterance'].lower() in CHOOSE['random']:
            base_workouts(req, res)
        if req['request']['original_utterance'].lower() in CHOOSE['random']:
            base_workouts(req, res)


def start(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Случайная тренировка.",
                "Моя тренировка.",
            ]
        }
        # Заполняем текст ответа
        res['response']['text'] = 'Привет! Со мной ты будешь тренироваться с максимальной эффективностью! Ты добавишь свою тренировку или выберешь из предложенных?'
        # Получим подсказки
        res['response']['buttons'] = [{
            "title": "Случайная тренировка",
            "hide": True
        }, {
            "title": "Моя тренировка",
            "hide": True
        }]
        return


    def _buildRequest():
        pass


if __name__ == '__main__':
    main()
