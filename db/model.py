# -*- coding: utf-8 *-*
import cgi

from google.appengine.ext import db

from model_data import (
    CATEGORY,
    COLOR,
    COUNTRIES,
    LEVEL,
    MODEL,
    STATES,
    SIZE,
)


class TwitterProfile(db.Model):
    twitter_access_token_key = db.StringProperty()
    twitter_access_token_secret = db.StringProperty()
    nick = db.StringProperty()

    def nickname(self):
        return self.nick


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
    profile = db.ReferenceProperty(TwitterProfile)

    def __init__(self, *args, **kw):
        super(Attendee, self).__init__(*args, **kw)
        fields = ['name', 'surname', 'nick', 'email', 'tel', 'personal_page',
                    'company', 'company_page', 'biography']
        not_req_fields = ['nick', 'tel', 'personal_page', 'company',
                    'company_page', 'biography']
        for field in fields:
            attr = getattr(self, field)
            if attr:  # NoneTypes can't be escaped
                setattr(self, field, cgi.escape(attr, quote="True"))
            if field in not_req_fields and not attr:
                setattr(self, field, '')


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
    profile = db.ReferenceProperty(TwitterProfile)

    def __init__(self, *args, **kw):
        super(Talk, self).__init__(*args, **kw)
        fields = ['title', 'abstract', 'knowledge', 'notes']
        not_req_fields = ['knowledge', 'notes']
        for field in fields:
            attr = getattr(self, field)
            if attr:
                setattr(self, field, cgi.escape(attr, quote="True"))
            if field in not_req_fields and not attr:
                setattr(self, field, '')


class Tshirt(db.Model):
    userId = db.UserProperty()
    profile = db.ReferenceProperty(TwitterProfile)
    color = db.StringProperty(verbose_name='Color', choices=COLOR)
    model = db.StringProperty(verbose_name='Modelo*', choices=MODEL,
        required=True)
    size = db.StringProperty(verbose_name='Talle*', choices=SIZE, required=True)
    total = db.StringProperty(verbose_name=u'Cantidad*', required=True)

    def __init__(self, *args, **kw):
        super(Tshirt, self).__init__(*args, **kw)
        fields = ['color', 'size', 'total', 'model']
        not_req_fields = ['total']
        for field in fields:
            attr = getattr(self, field)
            if attr:
                setattr(self, field, cgi.escape(attr, quote="True"))
            if field in not_req_fields and not attr:
                setattr(self, field, '')
