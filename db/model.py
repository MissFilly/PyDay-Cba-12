# -*- coding: utf-8 *-*
from google.appengine.ext import db


class Attendee(db.Model):
    userId = db.UserProperty()
    name = db.StringProperty()
    surname = db.StringProperty()
    nick = db.StringProperty()
    email = db.StringProperty()
    level = db.StringProperty()
    country = db.StringProperty()
    state = db.StringProperty()
    tel = db.StringProperty()
    in_attendees = db.BooleanProperty()
    allow_contact = db.BooleanProperty()
    personal_page = db.StringProperty()
    company = db.StringProperty()
    company_page = db.StringProperty()
    biography = db.TextProperty()
    cv = db.BlobProperty()


class Talk(db.Model):
    userId = db.UserProperty()
    title = db.StringProperty()
    level = db.StringProperty()
    abstract = db.TextProperty()
    category = db.StringProperty()
    knowledge = db.TextProperty()
    notes = db.TextProperty()
