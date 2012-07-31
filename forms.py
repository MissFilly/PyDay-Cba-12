# -*- coding: utf-8 *-*

from google.appengine.ext.db import djangoforms

from db.model import Attendee


class AttendeeForm(djangoforms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['userId']
        model.country.default = 'Argentina'
        model.state.default = 'Cordoba'
        model.level.default = 'Principiante'
