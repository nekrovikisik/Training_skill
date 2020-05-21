import sys, random
from datetime import datetime
import db_api
from my_api import *

def state(sessionStorage, req, res):
    my_state = sessionStorage['state']
    if my_state == 'greetings':
        sessionStorage, req, res = greetings(sessionStorage, req, res)
    elif my_state == 'firstMeet':
        sessionStorage, req, res = firstMeet(sessionStorage, req, res)
    elif my_state == 'firstmeet_lunges':
        sessionStorage, req, res = firstmeet_lunges(sessionStorage, req, res)
    elif my_state == 'chooseType':
        sessionStorage, req, res = chooseType(sessionStorage, req, res)
    elif my_state == 'get_training':
        sessionStorage, req, res = get_training(sessionStorage, req, res)
    elif my_state == 'showWorkout_list':
        sessionStorage, req, res = showWorkout_list(sessionStorage, req, res)
    elif my_state == 'chooseWorkout':
        sessionStorage, req, res = choose_workout(sessionStorage, req, res)
    elif my_state == 'is_suit':
        sessionStorage, req, res = is_suit(sessionStorage, req, res)
    elif my_state == 'startTraining':
        sessionStorage, req, res = startTraining(sessionStorage, req, res)
    sessionStorage['res'] = True
    print(sessionStorage['res'], sessionStorage['state'])
    return sessionStorage, req, res

def firstMeet(sessionStorage, req, res):
    print('Привет! Мы тут здороваемся')
    res['response']['text'] = 'Привет! Со мной ты будешь тренироваться с максимальной эффективностью! ' \
                              'Сколько ты можешь отжаться от пола?'
    sessionStorage['user'] = {'pushups': -1, 'lunges': -1}
    sessionStorage['state'] = 'firstmeet_pushups'
    # sessionStorage['res'] = True
    return sessionStorage, req, res

def firstmeet_lunges(sessionStorage, req, res):
    print('firstmeet_lunges firstmeet_lunges firstmeet_lunges')
    # sessionStorage['res'] = True
    res['response']['text'] = random.choice(['Сколько выпадов на одну ногу, ты можешь сделать?',
              'Назови число выпадов на одну ногу, которое ты можешь выполнить.'])
    return sessionStorage, req, res


def greetings(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    user_id = sessionStorage['uid']
    last_entance = db_api.getLast_entrace(sessionStorage['db_session'], user_id)
    now = datetime.today()
    timePassed = now - last_entance
    if timePassed.days > 3:
        text = random.choice(
            [f'Привет! Мы не виделись {timePassed.days} дней, я соскучилась по тренировкам с тобой!',
             'Привет, {timePassed.days} дней без общения с тобой были мучительны. ']) + 'Сейчас мы тренируемся, проводим тестирование или любуемся статистике тренировок?'
    else:
        text = 'Привет! Ты хочешь провести тестирование, потренироваться или посмотреть на статистику своих тренирвоок?'
    res['response']['buttons'] = [{"title": "Тестирование", "hide": True},
                                  {"title": "Статистика", "hide": True},
                                  {"title": "Тренировка", "hide": True}]
    return sessionStorage, req, res


def chooseType(sessionStorage, req, res):
    print('chooseType from FIRSTREQUEST')
    res['response']['text'] = 'Ты хочешь провести тестирование, потренироваться или посмотреть на статистику своих тренирвоок?'
    res['response']['buttons'] = [{"title": "Тестирование", "hide": True},
                                  {"title": "Статистика", "hide": True},
                                  {"title": "Тренировка", "hide": True}]
    sessionStorage['res'] = True
    return sessionStorage, req, res


def get_training(sessionStorage, req, res):
    res['response'][
        'text'] = 'Ты добавишь свою тренировку или выберешь из предложенных?'
    res['response']['buttons'] = [{
        "title": "Случайная тренировка",
        "hide": True
    }, {
        "title": "Моя тренировка",
        "hide": True
    }]
    # sessionStorage['state'] = 'showWorkout_list'
    # sessionStorage['workout']['autor'] = 'vikisik'
    # sessionStorage['res'] = True
    return sessionStorage, req, res


def showWorkout_list(sessionStorage, req, res):
    workout_names = db_api.getWorkout_names(session=sessionStorage['db_session'], autor=sessionStorage['workout']['autor'])
    resp = random.choice(['Мы можем предложить следующие тренировки:', 'Вот тренировки:', 'Список тренировок: '])
    workout_list = '\n'.join([f'{i}. {workout_names[i - 1]} ' for i in range(1, len(workout_names) + 1)])
    question = random.choice(
        ['О какой ты хочешь узнать подробнее?', "Список упражнений из какой тренировки тебе показать?"])
    res['response']['text'] = resp + '\n' + workout_list + '\n' + question
    # res['response']['buttons'] = [{"title": str(i), "hide": True} for i in WORKOUTS]
    res['response']['buttons'] = [{"title": str(i), "hide": True} for i in range(1, len(workout_names))]
    return sessionStorage, req, res



def choose_workout(sessionStorage, req, res, workout_name):
    autor = sessionStorage['workout']['autor']
    workout_name = workout_name.title()
    exercises_list = db_api.getExercises_list(sessionStorage['db_session'], autor, workout_name)
    print('now u choose your workout ------ ', exercises_list)
    sessionStorage['workout'] = {'autor': autor, 'workout_name': workout_name, 'currentEx': 0}
    my_workout = getExercDict(exercises_list)


    num_ex = len(my_workout['name'])  # число упражнений в тренировке
    ex_list = []
    for i in range(1, num_ex + 1):
        ex_list.append(F"{str(i)}. {my_workout['name'][i - 1]}, "
                       F"{my_workout['rep'][i - 1]}x, {my_workout['rest'][i - 1]}с. отдыха. ")
    res['response']['text'] = workout_name + '\n' + '\n'.join((ex_list)) + 'Тебе подходит эта тренировка?'

    res['response']['buttons'] = [{
        "title": "Да",
        "hide": True
    }, {
        "title": "Нет, посмотреть другие",
        "hide": True
    }]
    return sessionStorage, req, res


def is_suit(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    pass


def startTraining(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    pass
