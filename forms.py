# -*- coding: utf-8 *-*

from google.appengine.ext.db import djangoforms

from db.model import (Attendee, Talk)


class AttendeeForm(djangoforms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['userId']
        model.country.default = 'Argentina'
        model.state.default = 'Cordoba'
        model.level.default = 'Principiante'


class TalkForm(djangoforms.ModelForm):
    class Meta:
        model = Talk
        exclude = ['userId']
        model.level.default = 'Principiante'