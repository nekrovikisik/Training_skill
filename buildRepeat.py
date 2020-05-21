import sys
import random


def state(sessionStorage, req, res):
    my_state = sessionStorage['state']
    if my_state == 'firstmeet_pushups':
        sessionStorage, req, res = firstmeet_pushups(sessionStorage, req, res)
    if my_state == 'firstmeet_lunges':
        sessionStorage, req, res = firstmeet_pushups(sessionStorage, req, res)
    if my_state == 'chooseType':
        sessionStorage, req, res = chooseType(sessionStorage, req, res)
    if my_state == 'get_training':
        sessionStorage, req, res = get_training(sessionStorage, req, res)
    if my_state == 'showWorkout_list':
        sessionStorage, req, res = showWorkout_list(sessionStorage, req, res)
    if my_state == 'chooseWorkout':
        sessionStorage, req, res = choose_workout(sessionStorage, req, res)
    if my_state == 'is_suit':
        sessionStorage, req, res = is_suit(sessionStorage, req, res)
    if my_state == 'startTraining':
        sessionStorage, req, res = startTraining(sessionStorage, req, res)
    sessionStorage['repeat'] = False
    return sessionStorage, req, res


def firstmeet_pushups(sessionStorage, req, res):
    res['response']['text'] = random.choice(['Сколько раз ты можешь отжаться?',
                                             'Назови число отжиманий, которое ты можешь выполнить.'])
    sessionStorage['res'] = True
    return sessionStorage, req, res


def firstmeet_lunges(sessionStorage, req, res):
    res['response']['text'] = random.choice(['Сколько выпадов на одну ногу, ты можешь сделать?',
                                             'Назови число выпадов на одну ногу, которое ты можешь выполнить.'])
    sessionStorage['res'] = True
    return sessionStorage, req, res

def chooseType(sessionStorage, req, res):
    res['response']['text'] = 'Извини, я тебя не понимаю. Нажми на кнопку.'
    res['response']['buttons'] = [{
        "title": "Тестирование",
        "hide": True
    }, {
        "title": "Статистика",
        "hide": True
    }, {
        "title": "Тренировка",
        "hide": True
    }]
    sessionStorage['res'] = True
    return sessionStorage, req, res


def get_training(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    return sessionStorage, req, res



def showWorkout_list(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    return sessionStorage, req, res


def choose_workout(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    return sessionStorage, req, res


def is_suit(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    return sessionStorage, req, res


def startTraining(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    return sessionStorage, req, res
