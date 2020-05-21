import pymorphy2
import db_api

def user_id(req):
    return req['session']['user_id']


def app_id(req):
    return req["application"]["application_id"]


def getUserId(req):
    global sessionStorage
    try:
        uid = user_id(req)
    except:
        uid = app_id(req)
    return uid


def is_new_session(req):
    return bool(req['session']['new'])

def processing_num(sessionStorage, req, res):
        try:
            my_num = [i for i in req['request']['nlu']["entities"] if i['type'] == "YANDEX.NUMBER"]
            my_num = my_num[0]["value"]
        except:
            if req['request']['original_utterance'].isalnum():
                my_num = 5
            else:
                sessionStorage['repeat'] = True
                my_num = -1
        return sessionStorage, req, res


def getNormal_tokens(req):  # НОРМАЛИЗАЦИЯ самая полезная функция
    morph = pymorphy2.MorphAnalyzer()
    my_text = req['request']['original_utterance'].lower()
    # ASCII-коды букв кириллицы, цифр и пробела
    ordSymbols = list(list(range(1072, 1104)) + [ord(' ')] + [ord(str(i)) for i in range(1, 10)])
    words = [i for i in my_text if ord(i) in ordSymbols]  # очистка от знаков препинания
    words = ''.join(words).split(' ')
    tokens = []
    for i in words:
        if i.isalpha():
            tokens.append(morph.parse(i)[0].normal_form)
        elif i.isnumeric():
            tokens.append(i)
    print('getNormal_tokens : ', tokens)
    return tokens

def getExercDict(exercises_list):  # на выходе словарь тренировки
    my_keys = exercises_list[0]._asdict().keys()
    exerc_dict = {key: [exercises_list[0]._asdict()[key]] for key in my_keys}
    for workout in exercises_list[1:]:
        workout = workout._asdict()
        for key in exerc_dict.keys():
            exerc_dict[key].append(workout[key])
    return exerc_dict


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

def getYaNUM(req):
    my_num = [i for i in req['request']['nlu']["entities"] if i['type'] == "YANDEX.NUMBER"]
    my_num = my_num[0]["value"]
    return my_num