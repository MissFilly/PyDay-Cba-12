# -*- coding: utf-8 *-*

from google.appengine.ext.db import djangoforms

from db.model import (Attendee, Talk)


class AttendeeForm(djangoforms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['userId', 'profile']
        model.country.default = 'Argentina'
        model.state.default = 'Cordoba'
        model.level.default = 'Principiante'


class TalkForm(djangoforms.ModelForm):
    class Meta:
        model = Talk
        exclude = ['userId', 'profile']
        model.level.default = 'Principiante'
