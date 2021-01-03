# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
import string
# Импортируем модули для работы с JSON и логами и redis.
import json
import logging
import redis
# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

import os
import datetime
import icalendar
import DateParser.get_events
from Schedule import get_schedule_by_date, get_time_first_lesson

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}


# Задаем параметры приложения Flask.
@app.route('/', methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        'version': request.json['version'],
        'session': request.json['session'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']
    state = None
    facultet = None
    kafedra = None
    group = None
    db = redis.StrictRedis(host='localhost', port=6379, db=0)
    data = db.get(user_id)
    if data and len(str(data.decode()).split(':')) == 5:
        data = str(data.decode())
        state = data.split(':')[0]
        group = data.split(':')[0]

    else:
        if data is None:
            state = 'welcome'
        else:
            data = str(data.decode())
            state = data.split(':')[0]

    AK = ['ак', 'ока', 'аэрокосмический', 'аэрокосмическая', 'акогда', 'как', 'космонавты']
    BMT = ['бмт', 'бмд', 'бнт', 'бмто', 'бэнто', 'биомедицинскаятехника', 'биомедицинская', 'биологи']
    IBM = ['ибм', 'ибп', 'abm', 'iban', 'ibm', 'инженерный', 'бизнес', 'менеджмент', 'инженерныйбизнесименеджмент',
           'бизнесменеджмент', 'инженерныйбизнесменеджмент']
    IU = ['иу', 'йоу', 'иву', 'иум', 'ио', 'иван', 'иу', 'информатика', 'информатикаисистемыуправления',
          'информатикасистемыуправления', 'информационноеуправление', 'информационная', 'изюм']
    MT = ['мт', 'мета', 'машиностроительныетехнологии', 'технологиимашиностроения', 'машиностроение', 'мтс', 'мта',
          'мрт']
    RK = ['рк', 'робототехникаикомплекснаяавтоматизация', 'робототехника', 'комплекснаяавтоматизация', 'автоматизация',
          'робототехникакомплекснаяавтоматизация', 'вк', 'рпа', 'река']
    RL = ['рл', 'орел', 'орёл', 'рфпл', 'радиоэлектроника', 'радиоэлектроникаилазернаятехника', 'лазернаятехника',
          'лазеры', 'радиоэлектроникалазерная']
    RT = ['рт', 'радиотехнический', 'радиотехника']
    SGN = ['сгн', 'социальныеигуманитарныенауки', 'соцгум', 'скф', 'социальные', 'гуманитарныенауки', 'гуманитарии']
    SM = ['см', 'специальноемашиностроение', 'машиностроение', 'специальное', 'эм']
    FN = ['фн', 'фм', 'эфэн', 'фэн', 'фен', 'фнл', 'фена', 'ванна', 'фундаментальныенауки', 'фундаментальнаянаука',
          'фундаментальные', 'фундаментальная', 'наука', 'науки', 'ботаны']
    E = ['э', 'да', 'гей', 'энерго', 'энергеты', 'энергомашиностроение', 'энергомашиностроения']
    YR = ['юр', 'юриспруденцияинтеллектуальнаясобственностьисудебнаяэкспертиза', 'судебнаяэкспертиза', 'юриспруденция',
          'интеллектуальнаясобственность', 'собственность', 'экспертиза', 'юля', 'юристы']
    error = ["ошибка", "неправильно", "промах", "оплошность", "оплошка", "просчет", "погрешность", "ляпсус", "грех",
             "заблуждение", "неловкость", "опечатка", "описка", "отступление", "уклонение", "упущение",
             "неправильность", "шероховатость", "ложный шаг", "провес", "промер", "просмотр", "просчёт", "аномалия",
             "уродливость", "недостаток", "неосторожность", "преступление", "проруха", "аберрация", "накладка",
             "недогляд", "обман", "тавтология", "ослепление", "гистерология", "искажение", "неверный шаг", "паралогизм",
             "оговорка", "обольщение", "ослышка", "обмолвка", "неверность", "пропуск", "помарка", "промашка",
             "ошибочка", "обсчет", "парахронизм", "перлы", "провинность", "зевок", "прегрешение", "недоработка",
             "самообман", "прочет", "коллимация", "иллюзия", "недосмотр", "обвес", "неточность", "перекос",
             "самообольщение"]
    bakalavr = ["бакалавр", "бакалавриат"]
    aspirant = ["аспирант", "аспирантура"]
    magistr = ["магистр", "магистратура"]
    stepeni = [bakalavr, aspirant, magistr]
    facultet_buttons = [  # TODO: расположить в порядке популярности
        {'title': 'АК', 'hide': True},
        {'title': 'БМТ', 'hide': True},
        {'title': 'ИБМ', 'hide': True},
        {'title': 'ИУ', 'hide': True},
        {'title': 'МТ', 'hide': True},
        {'title': 'РК', 'hide': True},
        {'title': 'РЛ', 'hide': True},
        {'title': 'РТ', 'hide': True},
        {'title': 'СГН', 'hide': True},
        {'title': 'СМ', 'hide': True},
        {'title': 'ФН', 'hide': True},
        {'title': 'Э', 'hide': True},
        {'title': 'ЮР', 'hide': True}
    ]

    number_caf_buttons = [
        {'title': '1', 'hide': True},
        {'title': '2', 'hide': True},
        {'title': '3', 'hide': True},
        {'title': '4', 'hide': True},
        {'title': '5', 'hide': True},
        {'title': '6', 'hide': True},
        {'title': '7', 'hide': True},
        {'title': '8', 'hide': True},
        {'title': '9', 'hide': True},
        {'title': '10', 'hide': True},
        {'title': '11', 'hide': True},
        {'title': '12', 'hide': True},
        {'title': '13', 'hide': True}
    ]

    degree_buttons = [
        {'title': 'Бакалавр', 'hide': True},
        {'title': 'Магистр', 'hide': True},
        {'title': 'Аспирант', 'hide': True}
    ]

    base_buttons = [
        {'title': 'Какие сегодня пары?', 'hide': True},
        {'title': 'Какие завтра пары?', 'hide': True},
        {'title': 'Какие пары послезавтра?', 'hide': True},
        {'title': 'Во сколько первая пара во втроник?', 'hide': True},
        {'title': 'Во сколько заканчиваются пары 25 ноября', 'hide': True},
        {'title': 'Сменить группу', 'hide': True},
        {'title': 'Какие пары в понедельник?', 'hide': True},
        {'title': 'Какие во вторник?', 'hide': True},
        {'title': 'Какие пары в среду?', 'hide': True},
        {'title': 'Какие пары в четверг?', 'hide': True},
        {'title': 'Какие пары в пятницу?', 'hide': True},
        {'title': 'Какие пары в субботу?', 'hide': True},
        {'title': 'Какие пары в воскресение?', 'hide': True},

    ]

    if state == 'base':
        facultet = str(db.get(user_id).decode()).split(':')[1]
        cafedra_number = str(db.get(user_id).decode()).split(':')[2]
        group_number = str(db.get(user_id).decode()).split(':')[3]
        degree = str(db.get(user_id).decode()).split(':')[4]
        group_id = str(facultet + cafedra_number + '-' + group_number + degree)

        if req['request']['original_utterance'] == 'Какие сегодня пары?':
            date_today = datetime.datetime.today().strftime('%Y-%m-%d')
            rasp = get_schedule_by_date(group_id, date_today)
            res['response']['text'] = rasp
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Какие завтра пары?':
            date_today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            rasp = get_schedule_by_date(group_id, date_today)
            res['response']['text'] = rasp
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Какие пары послезавтра?':
            date_today = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
            rasp = get_schedule_by_date(group_id, date_today)
            res['response']['text'] = rasp
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Какие пары в понедельник?':
            weekday = datetime.datetime.today().weekday() + 1
            weekday_target = 1
            if weekday_target >= weekday:
                date_today = (datetime.datetime.today() + datetime.timedelta(days=(weekday_target - weekday))).strftime(
                    '%Y-%m-%d')
            else:
                date_today = (datetime.datetime.today() + datetime.timedelta(
                    days=((7 - weekday + weekday_target)))).strftime('%Y-%m-%d')
            rasp = get_schedule_by_date(group_id, date_today)
            res['response']['text'] = rasp
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Какие во вторник?':
            weekday = datetime.datetime.today().weekday() + 1
            weekday_target = 2
            if weekday_target >= weekday:
                date_today = (datetime.datetime.today() + datetime.timedelta(days=(weekday_target - weekday))).strftime(
                    '%Y-%m-%d')
            else:
                date_today = (datetime.datetime.today() + datetime.timedelta(
                    days=((7 - weekday + weekday_target)))).strftime('%Y-%m-%d')
            rasp = get_schedule_by_date(group_id, date_today)
            res['response']['text'] = rasp
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Какие пары в среду?':
            weekday = datetime.datetime.today().weekday() + 1
            weekday_target = 3
            if weekday_target >= weekday:
                date_today = (datetime.datetime.today() + datetime.timedelta(days=(weekday_target - weekday))).strftime(
                    '%Y-%m-%d')
            else:
                date_today = (datetime.datetime.today() + datetime.timedelta(
                    days=((7 - weekday + weekday_target)))).strftime('%Y-%m-%d')
            rasp = get_schedule_by_date(group_id, date_today)
            res['response']['text'] = rasp
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Какие пары в четверг?':
            weekday = datetime.datetime.today().weekday() + 1
            weekday_target = 4
            if weekday_target >= weekday:
                date_today = (datetime.datetime.today() + datetime.timedelta(days=(weekday_target - weekday))).strftime(
                    '%Y-%m-%d')
            else:
                date_today = (datetime.datetime.today() + datetime.timedelta(
                    days=((7 - weekday + weekday_target)))).strftime('%Y-%m-%d')
            rasp = get_schedule_by_date(group_id, date_today)
            res['response']['text'] = rasp
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Какие пары в пятницу?':
            weekday = datetime.datetime.today().weekday() + 1
            weekday_target = 5
            if weekday_target >= weekday:
                date_today = (datetime.datetime.today() + datetime.timedelta(days=(weekday_target - weekday))).strftime(
                    '%Y-%m-%d')
            else:
                date_today = (datetime.datetime.today() + datetime.timedelta(
                    days=((7 - weekday + weekday_target)))).strftime('%Y-%m-%d')
            rasp = get_schedule_by_date(group_id, date_today)
            res['response']['text'] = rasp + str(weekday_target - weekday)
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Какие пары в субботу?':
            weekday = datetime.datetime.today().weekday() + 1
            weekday_target = 6
            if weekday_target >= weekday:
                date_today = (datetime.datetime.today() + datetime.timedelta(days=(weekday_target - weekday))).strftime(
                    '%Y-%m-%d')
            else:
                date_today = (datetime.datetime.today() + datetime.timedelta(
                    days=((7 - weekday + weekday_target)))).strftime('%Y-%m-%d')
            rasp = get_schedule_by_date(group_id, date_today)
            res['response']['text'] = rasp
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Какие пары в воскресение?':
            res['response']['text'] = "В воскресение выходной! Ты что, совсем переучился?"
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Во сколько первая пара во втроник?':
            weekday = datetime.datetime.today().weekday() + 1
            weekday_target = 2
            if weekday_target >= weekday:
                date_today = (datetime.datetime.today() + datetime.timedelta(days=(weekday_target - weekday))).strftime(
                    '%Y-%m-%d')
            else:
                date_today = (datetime.datetime.today() + datetime.timedelta(
                    days=((7 - weekday + weekday_target)))).strftime('%Y-%m-%d')
            rasp = get_time_first_lesson(group_id, date_today)
            res['response']['text'] = 'Первая пара начинается в ' + rasp[:5]
            res['response']['buttons'] = base_buttons
            return

        if req['request']['original_utterance'] == 'Сменить группу':
            db.delete(user_id)
            state = 'welcome'
            res['response']['text'] = "Тогда назови факультет"
            res['response']['buttons'] = facultet_buttons
            return

        if req['request']['original_utterance']:
            res['response']['text'] = "Я умею отвечать только на вопросы о расписании!"
            res['response']['buttons'] = base_buttons
            return

    if state == 'welcome':
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        if req['request']['original_utterance'] == '':
            res['response'][
                'text'] = 'Привет! Я буду помогать тебе вспоминать к какой паре вставать или когда ты освободишься, а ещё я знаю всё расписание бауманки! А теперь назови свой факультет.'
            res['response']['buttons'] = facultet_buttons
            return

        facultets_sound = [AK, BMT, IBM, IU, MT, RK, RL, RT, SGN, SM, FN, E, YR]
        facultet_name = req['request']['original_utterance'].rstrip(string.punctuation).lower().replace(' ', '')

        # Обрабатываем ответ пользователя.
        for facultet in facultets_sound:
            if facultet_name in facultet:
                state = 'get_facultet'
                res['response']['text'] = 'Ваш факультет ' + facultet[
                    0].upper() + '? Если всё верно то назови номер кафедры. Если произошла ошибка скажите об этом.'
                facultet = facultet[0].upper()
                db.set(user_id, str(state + ":" + facultet))

                res['response']['buttons'] = number_caf_buttons
                return

        # Если не поняли то говорим
        if state == 'welcome':
            res['response']['text'] = 'Извините я не понимаю! Назови свой факультет'
            res['response']['buttons'] = facultet_buttons
            return
    if state == 'get_facultet':

        if req['request']['original_utterance'].rstrip(string.punctuation).lower().replace(' ', '') in error:
            res['response']['text'] = 'Извини, давай попробуем ещё раз. Какой у тебя факультет?'
            res['response']['buttons'] = facultet_buttons
            db.delete(user_id)
            state = 'welcome'
            return

        try:
            cafedra_number = int(
                ''.join(req['request']['nlu']['tokens']).rstrip(string.punctuation).lower().replace(' ', ''))
        except ValueError:
            res['response']['text'] = 'Нужно назвать только номер кафедры например для ИУ3 скажи 3. а ты сказал' + \
                                      req['request']['original_utterance'].rstrip(string.punctuation).lower().replace(
                                          ' ', '')
            res['response']['buttons'] = number_caf_buttons
            return
        cafedra_number = str(cafedra_number)
        facultet = str(db.get(user_id).decode()).split(':')[1]
        state = 'get_cafedra'
        db.set(user_id, str(state + ":" + facultet + ":" + cafedra_number))
        res['response'][
            'text'] = 'Твоя кафедра ' + facultet + cafedra_number + ' верно? Теперь нужно назвать номер группы!'
        return

    if state == 'get_cafedra':

        if req['request']['original_utterance'].rstrip(string.punctuation).lower().replace(' ', '') in error:
            res['response']['text'] = 'Извини, давай попробуем ещё раз. Какой у тебя факультет?'
            res['response']['buttons'] = facultet_buttons
            db.delete(user_id)
            state = 'welcome'
            return

        try:
            group_number = int(
                ''.join(req['request']['nlu']['tokens']).rstrip(string.punctuation).lower().replace(' ', ''))
        except:
            res['response']['text'] = 'Нужно назвать номер твоей группы, например для ИУ3-71 скажи 71.'
            # res['response']['buttons'] = number_caf_buttons
            return
        group_number = str(group_number)
        facultet = str(db.get(user_id).decode()).split(':')[1]
        cafedra_number = str(db.get(user_id).decode()).split(':')[2]
        state = 'get_group'
        db.set(user_id, str(state + ":" + facultet + ":" + cafedra_number + ":" + group_number))
        res['response'][
            'text'] = 'Твоя группа ' + facultet + cafedra_number + '-' + group_number + ' верно? Осталось сказать Бакалавр ты Аспирант или же Магистр! Выбирай с умом!'
        res['response']['buttons'] = degree_buttons
        return

    if state == 'get_group':

        if req['request']['original_utterance'].rstrip(string.punctuation).lower().replace(' ', '') in error:
            res['response']['text'] = 'Извини, давай попробуем ещё раз. Какой у тебя факультет?'
            res['response']['buttons'] = facultet_buttons
            db.delete(user_id)
            state = 'welcome'
            return

        stepen_name = req['request']['original_utterance'].rstrip(string.punctuation).lower().replace(' ', '')
        facultet = str(db.get(user_id).decode()).split(':')[1]
        cafedra_number = str(db.get(user_id).decode()).split(':')[2]
        group_number = str(db.get(user_id).decode()).split(':')[3]
        for stepen in stepeni:
            if stepen_name in stepen:
                state = 'base'
                group_id = str(facultet + cafedra_number + '-' + group_number + stepen_name.upper()[0])
                files = os.listdir("./Groups/")
                if str(group_id + ".ics") not in files:
                    db.set(user_id, str(state + ":" + facultet + ":" + cafedra_number + ":" + group_number + ":" + "Л"))
                    if str(group_id[:-1] + "Л.ics") not in files:
                        res['response'][
                            'text'] = 'Извини, я не нахожу твою группу, давай попробуем ещё раз. Какой у тебя факультет?'
                        res['response']['buttons'] = facultet_buttons
                        db.delete(user_id)
                        state = 'welcome'
                        return
                else:
                    db.set(user_id, str(state + ":" + facultet + ":" + cafedra_number + ":" + group_number + ":" + str(
                        stepen_name.upper()[0])))
                    if str(group_id + ".ics") not in files:
                        res['response'][
                            'text'] = 'Извини, я не нахожу твою группу, давай попробуем ещё раз. Какой у тебя факультет?'
                        res['response']['buttons'] = facultet_buttons
                        db.delete(user_id)
                        state = 'welcome'
                        return

                # res['response']['buttons'] = base_buttons

        if state == 'get_group':
            res['response']['text'] = 'Нужно сказать Бакалавр ты Магистр или Аспирант.'
            res['response']['buttons'] = degree_buttons
            return

        degree = str(db.get(user_id).decode()).split(':')[4]
        if degree == "Л":
            res['response'][
                'text'] = 'Твоя группа ' + facultet + cafedra_number + '-' + group_number + ' верно? Теперь ты можешь спрашивать меня о расписании. Также ты можешь в любой момент сменить группу!'
            res['response']['buttons'] = base_buttons
            return
        res['response'][
            'text'] = 'Твоя группа ' + facultet + cafedra_number + '-' + group_number + degree + ' верно? Теперь ты можешь спрашивать меня о расписании. Также ты можешь в любой момент сменить группу!'
        res['response']['buttons'] = base_buttons
        return


app.run(ssl_context='adhoc', host='0.0.0.0', port=5000)
