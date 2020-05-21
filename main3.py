# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
import  gunicorn
from datetime import datetime
import random
import pymorphy2
from flask import Flask, request

import logging
import json

from data import db_session
from data.exercises import Exercises
from data.workouts import Workouts
from data.users import Users
from data.db_session import SqlAlchemyBase
from user import User

morph = pymorphy2.MorphAnalyzer()
user = True

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)  # уровень логирования

sessionStorage = {'repeat': False, 'res': False}
# для каждой сессии общения хранятся подсказки, которые видел пользователь.
# (buttons в JSON ответа).
CHOOSE = {'random': ['случайная', 'рандом', 'все равно', 'своя', 'собственная', 'моя'],
          'firstmeet': ['start', 'firstmeet_pushups', 'firstmeet_lunges']}
db_session.global_init("db/Exercises.sqlite")
session = db_session.create_session()


def WORKOUTS(autor='vikisik'):
    all_w = session.query(Workouts.name).filter(Workouts.ex_id == Exercises.id, Workouts.autor == autor).all()
    all_w = sorted(list(set(all_w)))
    return [i[0].lower() for i in all_w]


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
    print(request.json['request']['original_utterance'].lower())
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def handle_dialog(req, res):
    global user


    if not is_new_session(req):
        print('This id new session')
        if is_new_user(req):
            print('THIS USER IS NEW')
            user = User(uid=user_id(req))
              # добавляем в sessionStorage userid
            sessionStorage['state'] = 'firstMeet'
            firstMeet(req, res)
        else:
            sessionStorage['state'] = 'greetings'
            greetings(req, res)
    else:
        if 'гусь' in req['request']['original_utterance'].lower() or 'uecm' in req['request'][
            'original_utterance'].lower():
            print('get_training')
            get_training(req, res)
        else:
            if 'выход' in req['request']['nlu']['tokens']:  # если человек хочет выйти
                res['response']['text'] = 'Пока-пока!'
                res["response"] = {"end_session": False}
            else:
                print('sessionStorage[state] == ', sessionStorage['state'])
                # set_state()
                if sessionStorage['state'] in CHOOSE['firstmeet']:  # если человек впервые в навыке
                    firstMeet(req, res)  # знакомимся
                    # после знакомства/ во время входа
                elif sessionStorage['state'] == 'choose type':
                    get_training(req, res)
                elif sessionStorage['state'] == 'get_training':
                    get_training(req, res)
                elif sessionStorage['state'] == 'showWorkout_list':
                    showWorkout_list(req, res)
                elif sessionStorage['state'] == 'choose workout':
                    choose_workout(req, res)
                elif sessionStorage['state'] == 'is_suit':
                    is_suit(req, res)
                elif sessionStorage['state'] == 'startTraining':
                    startTraining(req, res)
    #setLast_entance(user_id(req))
    user.set_state(sessionStorage['state'])

# def set_state(): # эта функция закидывает стейт в бд
#     state = sessionStorage['state']
#     my_uid = user_id(req)


# def setUserId(req):
#     try:
#         user_id(req) = user_id(req)
#     except:
#         user_id(req) = app_id(req)
#     print('ACHTUNG USER ID', user_id(req))


def addUser(uid):
    user = Users()
    user.uid = uid
    user.state = 'firstMeet'
    user.last_entrace = datetime.today()

    session.add(user)
    session.commit()


def setLast_entance(uid):
    rows = session.query(Users).filter(Users.uid == uid).update({'last_entrace': datetime.today()})
    session.commit()


def is_new_session(req):
    return bool(req['session']['new'])


def is_new_user(req):
    # uid = setUserId(req)
    uid = user_id(req)
    return not (session.query(Users.uid).filter(Users.uid == uid).first())


def greetings(req, res):
    if sessionStorage['res'] == False:
        last_entance = session.query(Users.last_entrace).filter(Users.uid == user_id).first()[0]
        now = datetime.today()
        timePassed = now - last_entance
        if timePassed.days > 3:
            text = random.choice(
                [f'Привет! Мы не виделись {timePassed.days} дней, я соскучилась по тренировкам с тобой!',
                 'Привет, {timePassed.days} дней без общения с тобой были мучительны. '])
            text = text + 'Сейчас мы тренируемся, проводим тестирование или любуемся статистике тренировок?'
        else:
            text = 'Привет! Ты хочешь провести тестирование, потренироваться или посмотреть на статистику своих тренирвоок?'

        res['response']['text'] = text

        res['response']['buttons'] = [{"title": "Тестирование", "hide": True},
                                      {"title": "Статистика", "hide": True},
                                      {"title": "Тренировка", "hide": True}]
    else:
        tokens = getNormal_tokens(req)
        if 'тестирование' in tokens:
            pass
        elif 'статистика' in tokens:
            pass
        elif 'тренировка' in tokens:
            get_training(req, res)
        else:
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


def getNormal_tokens(req):  # НОРМАЛИЗАЦИЯ самая полезная функция
    print('getNormal_tokens')
    my_text = req['request']['original_utterance']

    all(list(filter(lambda x: (x.isnumeric()), ['о', 'пятой'])))

    if all(list(map(lambda x: (True if x.isnumeric() else False), my_text.split()))):  # введено число/ числа
        print('getNormal_tokens: введено число/ числа')
        print(my_text.split())
        return my_text.split()
    else:  # есть буквы
        print('getNormal_tokens: есть буквы')

        my_text = my_text.lower()
        ordSymbols = list(list(range(1072, 1104)) + [ord(' ')] + [ord(str(i)) for i in range(1,
                                                                                             10)])  # ASCII-коды букв кириллицы, цифр и пробела
        words = [i for i in my_text if ord(i) in ordSymbols]  # очистка от знаков препинания
        print(words)
        words = ''.join(words)
        print(words)
        words = ''.join(words).split(' ')
        print(words)
        tokens = []
        for i in words:
            if i.isalpha():
                tokens.append(morph.parse(i)[0].normal_form)
            elif i.isnumeric() or i.isalnum():
                tokens.append(i)
        print('getNormal_tokens : ', tokens)
        return tokens


def getExercises(workout_name, autor='vikisik'):  # на выходе словарь тренировки
    print(workout_name, autor)
    print(session.query(Workouts.num_id, Exercises.name, Workouts.ex_id, Exercises.about, Workouts.rep,
                        Workouts.rest).filter(
        Workouts.name == workout_name, Workouts.ex_id == Exercises.id,
        Workouts.autor == autor).all()
          )
    # INPUT: объект класса тренировки
    # OUTPUT: {'id': [номера упраж из Exercises], 'name': [названия упраж],'about': [доп. инфа], img_url = url пикчи}
    exercises_list = session.query(Workouts.num_id, Exercises.name, Workouts.ex_id, Exercises.about, Workouts.rep,
                                   Workouts.rest).filter(
        Workouts.name == workout_name, Workouts.ex_id == Exercises.id,
        Workouts.autor == autor).all()
    print(exercises_list)
    my_keys = exercises_list[0]._asdict().keys()
    exerc_dict = {key: [exercises_list[0]._asdict()[key]] for key in my_keys}
    for workout in exercises_list[1:]:
        workout = workout._asdict()
        for key in exerc_dict.keys():
            exerc_dict[key].append(workout[key])
    return exerc_dict


def choose_workout(req, res, workout_name, autor='vikisik'):  # state: choose_workout
    workout_name = workout_name.title()
    my_workout = getExercises(workout_name)
    print('now u choose your workout ------ ', my_workout)
    sessionStorage['workout'] = {'autor': autor, 'workout_name': workout_name, 'currentEx': 0}
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
    sessionStorage['state'] = 'is_suit'

def getWorkout_list(req):
    tokens = getNormal_tokens(req)
    if set(['предложенный', 'случайная', 'равно', 'пофиг' ]) & set(tokens):
        autor = 'vikisik'
        return autor
    elif set(['мой', 'свой', 'собственная', 'добавить']) & set(tokens):
        autor = req[user_id]
        return autor
    else:
        sessionStorage['repeat'] = True



def showWorkout_list(req, res):
    workout_names = WORKOUTS()
    if sessionStorage['res'] == False:
        resp = random.choice(['Мы можем предложить следующие тренировки:', 'Вот тренировки:', 'Список тренировок: '])
        workout_list = '\n'.join([f'{i}. {workout_names[i - 1]} ' for i in range(1, len(workout_names) + 1)])
        question = random.choice(
            ['О какой ты хочешь узнать подробнее?', "Список упражнений из какой тренировки тебе показать?"])
        res['response']['text'] = resp + '\n' + workout_list + '\n' + question
        # res['response']['buttons'] = [{"title": str(i), "hide": True} for i in WORKOUTS]
        res['response']['buttons'] = [{"title": str(i), "hide": True} for i in range(1, len(workout_names))]
        sessionStorage['res'] = True

    elif sessionStorage['res'] == True:
        tokens = getNormal_tokens(req)
        choosed_w = list(filter(lambda x: (x in workout_names), tokens))
        print('choosed_w', choosed_w)
        if choosed_w:
            num = workout_names.index(choosed_w[0])
        else:
            print('numWorkout_treatment')
            num = numWorkout_treatment(tokens)
            choose_workout(req, res, workout_names[int(num)].title(), autor='vikisik')

        try:
            print(num)
            workout_name = workout_names[int(num) - 1]
            print('my_workout ', workout_name)
            choose_workout(req, res, workout_name.title())
        except:
            res['response'][
                'text'] = 'Я не понимаю, назови номер тренировки. блин тупица нормально говори еще обработчик писать'
        finally:
            sessionStorage['res'] = False


def numWorkout_treatment(tokens):
    print(tokens)
    numerals = {'первый': 1, 'второй': 2, 'третий': 3, 'четвертый': 4, 'пятый': 5, 'шестой': 6, 'седьмой': 7,
                'восьмой': 8, 'девятый': 9}
    nums = list(numerals.keys())
    if set(nums) & set(tokens):
        k = list(set(nums) & set(tokens))[0]  # если сказано порядковое числительное
        num = numerals[k]
    elif {'1', '2', '3', '4', '9', '6', '7', '8', '5'} & set(tokens):
        print('set(tokens)= ', set(tokens))
        print({'1', '2', '3', '4', '9', '6', '7', '8', '5'} & set(tokens))
        num = list({'1', '2', '3', '4', '9', '6', '7', '8', '5'} & set(tokens))[0]
    return num


def is_suit(req, res):
    print('is_suit')
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


def areYouReady(req, res):
    print('you reaady???')
    res['response']['text'] = 'Ну что, начинаем?'
    sessionStorage['state'] = 'areYouReady'
    res['response']['buttons'] = [{'title': 'Начинаем сейчас', 'hide': True},
                                  {'title': 'Давай позже.', 'hide': True}
                                  ]


def startTraining(req, res):
    res['response'][
        'text'] = 'фффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффф'
    print('She is ready ')


def user_id(req):
    return req['session']['user_id']


def app_id(req):
    return req["application"]["application_id"]


def firstMeet(req, res):
    if sessionStorage['state'] in ['firstmeet_pushups', 'firstmeet_lunges']:
        if sessionStorage['repeat']:  # если человек сказал фигню
            print('не гоpassвори ФИГНЮ')
            if sessionStorage['state'] == 'firstmeet_pushups':
                res['response']['text'] = random.choice(['Сколько раз ты можешь отжаться?',
                                                         'Назови число отжиманий, которое ты можешь выполнить.'])
            elif sessionStorage['state'] == 'firstmeet_lunges':
                res['response']['text'] = random.choice(['Сколько выпадов на одну ногу, ты можешь сделать?',
                                                         'Назови число выпадов на одну ногу, которое ты можешь выполнить.'])
            sessionStorage['repeat'] = False
        elif req['request']['original_utterance'] and not sessionStorage['repeat']:
            processing_info(req, res)
    else:
        print('Привет! Мы тут здороваемся')
        if 'info' not in list(sessionStorage.keys()):  # здороваемся
            res['response']['text'] = 'Привет! Со мной ты будешь тренироваться с максимальной эффективностью! ' \
                                      'Сколько ты можешь отжаться от пола?'
           # sessionStorage['user'] = {'pushups': -1, 'lunges': -1}
            sessionStorage['state'] = 'firstmeet_pushups'


def processing_info(req, res):
    # если человек назвал хоть какое-то число
    #try:
        my_num = [i for i in req['request']['nlu']["entities"] if i['type'] == "YANDEX.NUMBER"]
        my_num = my_num[0]["value"]
        print(my_num)
        if sessionStorage['state'] == 'firstmeet_pushups':
            #try:
                #sessionStorage['user']['pushups'] = my_num[-1]
                user.set_pushups(my_num)
            #except:
            #    sessionStorage['user']['pushups'] = my_num
            #finally:
                sessionStorage['state'] = 'firstmeet_lunges'
                print('now: finally   ', sessionStorage['state'])
                res['response']['text'] = 'Отлично! Теперь скажи, сколько выпадов ты можешь сделать на каждую ногу?'

        elif sessionStorage['state'] == 'firstmeet_lunges':
                user.set_lunges(my_num)
     #       try:
     #           sessionStorage['user']['lunges'] = my_num[-1]
     #       except:
     #           sessionStorage['user']['lunges'] = my_num
     #       finally:
                sessionStorage['state'] = 'get_training'
                get_training(req, res)
    #except:
    #    sessionStorage['repeat'] = True
    #    firstMeet(req, res)


def get_training(req, res):
    # res['response']['buttons'] = {'suggests': ["Случайная тренировка.", "Моя тренировка.", ]}
    res['response'][
        'text'] = 'Ты добавишь свою тренировку или выберешь из предложенных?'
    res['response']['buttons'] = [{
        "title": "Случайная тренировка",
        "hide": True
    }, {
        "title": "Моя тренировка",
        "hide": True
    }]
    sessionStorage['state'] = 'showWorkout_list'
    return



if __name__ == '__main__':
    app.run(port=8888)
