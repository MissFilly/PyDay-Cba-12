# -*- coding: utf-8 *-*
from google.appengine.ext import db

from model_data import (
    CATEGORY,
    COUNTRIES,
    LEVEL,
    STATES,
)


class Attendee(db.Model):
    userId = db.UserProperty()
    name = db.StringProperty(verbose_name='Nombre*', required=True)
    surname = db.StringProperty(verbose_name='Apellido*', required=True)
    nick = db.StringProperty(verbose_name='Apodo')
    email = db.StringProperty(verbose_name='Email*', required=True)
    level = db.StringProperty(verbose_name='Conocimientos de Python',
        choices=LEVEL)
    country = db.StringProperty(verbose_name=u'País', choices=COUNTRIES)
    state = db.StringProperty(verbose_name='Provincia', choices=STATES)
    tel = db.StringProperty(verbose_name=u'Número de teléfono')
    in_attendees = db.BooleanProperty(
        verbose_name='Incluir en lista de participantes')
    allow_contact = db.BooleanProperty(
        verbose_name='Contacto con auspiciantes')
    personal_page = db.StringProperty(verbose_name='Página web personal')
    company = db.StringProperty(
        verbose_name='Nombre de entidad (empresa, universidad)')
    company_page = db.StringProperty(verbose_name=u'Página web de entidad')
    biography = db.TextProperty(verbose_name=u'Biografía (resumen)')
    cv = db.StringProperty(verbose_name='Link a descarga de CV')

    def __init__(self, *args, **kw):
        super(Attendee, self).__init__(*args, **kw)
        if not self.nick:
            self.nick = ''
        if not self.tel:
            self.tel = ''
        if not self.personal_page:
            self.personal_page = ''
        if not self.company:
            self.company = ''
        if not self.company_page:
            self.company_page = ''
        if not self.biography:
            self.biography = ''
        if not self.cv:
            self.cv = ''


class Talk(db.Model):
    userId = db.UserProperty()
    title = db.StringProperty(verbose_name=u'Título*', required=True)
    level = db.StringProperty(verbose_name='Nivel', choices=LEVEL)
    abstract = db.TextProperty(
        verbose_name=u'Descripción* (se mostrará a los asistentes)',
        required=True)
    category = db.StringProperty(verbose_name=u'Categoría', choices=CATEGORY)
    knowledge = db.TextProperty(
        verbose_name='Conocimientos previos requeridos')
    notes = db.TextProperty(verbose_name='Notas')

    def __init__(self, *args, **kw):
        super(Talk, self).__init__(*args, **kw)
        if not self.knowledge:
            self.knowledge = ''
        if not self.notes:
            self.notes = ''
