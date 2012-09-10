# -*- coding: utf-8 *-*

from google.appengine.ext.db import djangoforms

from db.model import (Attendee, Talk, Tshirt)


class AttendeeForm(djangoforms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['userId', 'profile', 'assist_dinner']
        model.country.default = 'Argentina'
        model.state.default = 'Cordoba'
        model.level.default = 'Principiante'


class TalkForm(djangoforms.ModelForm):
    class Meta:
        model = Talk
        exclude = ['userId', 'profile']
        model.level.default = 'Principiante'


class TshirtForm(djangoforms.ModelForm):
    class Meta:
        model = Tshirt
        exclude = ['userId', 'profile']
        model.color.default = 'Negro'
        model.total.default = '1'
        model.model.default = 'Hombre'
