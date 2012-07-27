# -*- coding: utf-8 *-*
import datetime


def days_left():
    date = datetime.datetime(2012, 9, 15)
    delta = date - date.now()
    return delta.days + 1


def days_left_message():
    days = days_left()
    message_text = None
    if days == 1:
        message_text = ('Falta', days, u'día')
    elif days == 0:
        message_text = (u'Asistí', 'HOY', 'al PyDay')
    else:
        message_text = ('Faltan', days, u'días')

    return message_text
