import sys
import firstRequest
from my_api import *

import buildRepeat


def state(sessionStorage, req, res):
    my_state = sessionStorage['state']
    if my_state == 'greetings':
        sessionStorage, req, res = greetings(sessionStorage, req, res)
    my_state = sessionStorage['state']
    if my_state == 'firstmeet_pushups':
        sessionStorage, req, res = firstmeet_pushups(sessionStorage, req, res)
    if my_state == 'firstmeet_lunges':
        print('ОБРАБОТКА ЗАПРОСА НА КОЛВО ВЫПАДОВ')
        sessionStorage, req, res = firstmeet_lunges(sessionStorage, req, res)
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
    try:
        my_num = getYaNUM(req)
        sessionStorage['user']['pushups'] = my_num
        sessionStorage['state'] = 'firstmeet_lunges'
        sessionStorage['res'] = False
        print(my_num, ' MYNUM')
    except:
        if req['request']['original_utterance'].isalnum():
            sessionStorage['user']['pushups'] = 5
            sessionStorage['state'] = 'firstmeet_lunges'
            sessionStorage['res'] = False
            print("sessionStorage['user']['pushups'] = ", 5)
        else:
            print("sessionStorage['repeat']  ", sessionStorage['repeat'])
            sessionStorage['repeat'] = True
            sessionStorage, req, res = buildRepeat.state(sessionStorage, req, res)
            return sessionStorage, req, res
    print('firstRequest.state(sessionStorage, req, res)  ', sessionStorage['state'])
    sessionStorage['res'] = False
    return firstRequest.state(sessionStorage, req, res)
    # return sessionStorage, req, res


def firstmeet_lunges(sessionStorage, req, res):
    try:
        my_num = [i for i in req['request']['nlu']["entities"] if i['type'] == "YANDEX.NUMBER"]
        my_num = my_num[0]["value"]
        sessionStorage['user']['lunges'] = my_num

        sessionStorage['state'] = 'chooseType'
        sessionStorage['res'] = False
        sessionStorage, req, res = firstRequest.state(sessionStorage, req, res)

        print('firstmeet_lunges    ', 'MYNUM   ',my_num,  sessionStorage['state'] )
    except:
        if req['request']['original_utterance'].isalnum():
            sessionStorage['user']['lunges'] = 5

            sessionStorage['res'] = False
            sessionStorage['state'] = 'chooseType'
            sessionStorage, req, res = firstRequest.state(sessionStorage, req, res)
            # sessionStorage['res'] = False
        else:
            sessionStorage['repeat'] = True
            sessionStorage, req, res = buildRepeat.state(sessionStorage, req, res)
    return sessionStorage, req, res


def greetings(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    pass


def chooseType(sessionStorage, req, res):
    print('chooseType from HANDLERESPONCE')
    tokens = getNormal_tokens(req)
    print('tokens from getNormal_tokens: ', tokens)
    if 'тестирование' in tokens:
        pass
    elif 'статистика' in tokens:
        pass
    elif 'тренировка' in tokens:
        sessionStorage['state'] = 'get_training'
        sessionStorage['res'] = False
        sessionStorage, req, res = firstRequest.state(sessionStorage, req, res)
    else:
        sessionStorage['repeat'] = True
        sessionStorage, req, res = buildRepeat.state(sessionStorage, req, res)
    return sessionStorage, req, res





def get_training(sessionStorage, req, res):
    tokens = getNormal_tokens(req)
    repeat = False
    if set(['предложенный', 'случайная', 'равно', 'пофига']) & set(tokens):
        sessionStorage['workout'] = {'autor':'vikisik'}
    elif set(['мой', 'свой', 'собственная', 'добавить']) & set(tokens):
        sessionStorage['workout'] = {'autor':req[user_id]}
    else:
        return repeat(sessionStorage, req, res)

    sessionStorage['state'] = 'showWorkout_list'
    sessionStorage, req, res = firstRequest.showWorkout_list(sessionStorage, req, res)
    return sessionStorage, req, res


def showWorkout_list(sessionStorage, req, res):
    tokens = getNormal_tokens(req)
    workout_names = db_api.getWorkout_names(session=sessionStorage['db_session'], autor=sessionStorage['workout']['autor'])
    print(workout_names)
    choosed_w = list(filter(lambda x: (x in workout_names), tokens))
    print('choosed_w', choosed_w)
    if choosed_w: # если назвали тренировку словом
        num = workout_names.index(choosed_w[0])
    elif getYaNUM(req): # если нажали на числовую кнопку
        num = getYaNUM(req)
    else:
        return repeat(sessionStorage, req, res)
    sessionStorage['res'] = False
    sessionStorage, req, res = firstRequest.choose_workout(sessionStorage, req, res, workout_names[num - 1])
    return sessionStorage, req, res

def choose_workout(sessionStorage, req, res):
        print('choose_workout')
        variables = {'да': ['да', 'подходить', 'конечно', 'ага', 'давай'], 'нет': ['нет', 'не', 'посмотреть', 'другие']}
        tokens = getNormal_tokens(req)

        if set(tokens) & set(variables['нет']):
            print(set(tokens) & set(variables['нет']))
            showWorkout_list(req, res)
            sessionStorage['state'] = 'showWorkout_list'
            sessionStorage['res'] = False
        elif set(tokens) & set(variables['да']):
            sessionStorage['state'] = 'startTraining'
            sessionStorage['res'] = False
            startTraining(req, res)
        else:
            sessionStorage['repeat'] = True
            sessionStorage['res'] = False


def is_suit(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    pass


def startTraining(sessionStorage, req, res):
    print(sys._getframe().f_code.co_name)
    pass

def repeat(sessionStorage, req, res):
    print("sessionStorage['repeat']  ", sessionStorage['repeat'])
    sessionStorage['repeat'] = True
    sessionStorage, req, res = buildRepeat.state(sessionStorage, req, res)
    return sessionStorage, req, res
