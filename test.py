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


def get_schedule_by_date(group, date):
    day_scedule = DateParser.get_events.get_events(group, date)
    return day_scedule


rasp = get_schedule_by_date("ИУ3-71Б", "2018-11-15")

print(rasp)
