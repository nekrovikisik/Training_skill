from __future__ import unicode_literals
import gunicorn
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

import buildRepeat
import handleResponce
import firstRequest
from my_api import *
from db_api import *

morph = pymorphy2.MorphAnalyzer()
user = True

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)  # уровень логирования


db_session.global_init("db/Exercises.sqlite")
session = db_session.create_session()

sessionStorage = {'state': 'greetings', 'repeat': False, 'res': False, 'currentTraining': False, 'db_session': session}


@app.route('/post', methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
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
    # Функция для непосредственной обработки диалога.
    if is_new_session(req):
        print('This is new session')
        if is_new_user(session, req):
            print('THIS USER IS NEW')
            #user = User(uid=user_id(req))
            # добавляем в sessionStorage userid
            sessionStorage['state'] = 'firstMeet'
            # firstMeet(req, res)
            # print('firstMeet')

        else:
            sessionStorage['state'] = 'greetings'
            print('greetings')

        sessionStorage['uid'] = getUserId(req)
    buildRequest(req, res)


def buildRequest(req, res):
    global sessionStorage
    print('Im build your request' + '\n'  + 'current STATE: '+ sessionStorage['state'] + '\n'  +'repeat: '  + str( sessionStorage['repeat'] ) + '\n'  +'res: '  + str( sessionStorage['res'] ))
    print('REQUEST: '+ req['request']['original_utterance'])
    if sessionStorage['repeat']:  # если юзер сказал фигню и алиса не поняла, она повторяет
        sessionStorage, req, res = buildRepeat.state(sessionStorage, req, res)
    elif sessionStorage['res']:  # если юзер хоть как-то ответил
        sessionStorage, req, res = handleResponce.state(sessionStorage, req, res)
    else: # если ответ еще не отправлен
        sessionStorage, req, res = firstRequest.state(sessionStorage, req, res)
    print(sessionStorage['res'], sessionStorage['state'])
    print()
    print()

if __name__ == '__main__':
    app.run()
