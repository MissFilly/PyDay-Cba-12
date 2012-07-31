# -*- coding: utf-8 *-*

import model


def add_attendee(attendee):
    """Register a new attendee in the database."""
    # Check if this user is already registered
    exist = model.Attendee.all()
    exist.filter('userId =', attendee.userId)
    if exist.count() != 0:
        return False

    if (attendee.personal_page and
       not attendee.personal_page.startswith('http://')):
        attendee.personal_page = 'http://%s' % attendee.personal_page
    if (attendee.company_page and
       not attendee.company_page.startswith('http://')):
        attendee.company_page = 'http://%s' % attendee.company_page

    attendee.put()
    return True


def update_attendee(registered_attendee):
    """Register a new attendee in the database."""
    # Check if this user is already registered
    attendee = model.Attendee.all()
    attendee.filter('userId =', registered_attendee.userId)
    if attendee.count() == 0:
        return False

    attendee = attendee[0]
    attendee.name = registered_attendee.name
    attendee.surname = registered_attendee.surname
    attendee.nick = registered_attendee.nick
    attendee.email = registered_attendee.email
    attendee.level = registered_attendee.level
    attendee.country = registered_attendee.country
    attendee.state = registered_attendee.state
    attendee.tel = registered_attendee.tel
    attendee.in_attendees = registered_attendee.in_attendees
    attendee.allow_contact = registered_attendee.allow_contact
    if (registered_attendee.personal_page and
       not registered_attendee.personal_page.startswith('http://')):
        attendee.personal_page = ('http://%s' %
            registered_attendee.personal_page)
    attendee.company = registered_attendee.company
    if (registered_attendee.company_page and
       not registered_attendee.company_page.startswith('http://')):
        attendee.company_page = 'http://%s' % registered_attendee.company_page
    attendee.company_page = registered_attendee.company_page
    attendee.biography = registered_attendee.biography
    attendee.cv = registered_attendee.cv

    attendee.put()
    return True


def add_talk(talk):
    """Register a new talk for the event."""
    # Check if this user is already registered
    attendee = model.Attendee.all()
    attendee.filter('userId =', talk.userId)
    if attendee.count() == 0:
        return False

    talk.put()
    return True


def update_talk(key, registered_talk):
    """Register a new talk for the event."""
    # Check if this user is already registered
    talks = model.Talk.all()
    talks.filter('userId =', registered_talk.userId)

    talk = None
    for t in talks:
        if str(t.key()) == key:
            talk = t
            break
    if talk is None:
        return False
    talk.title = registered_talk.title
    talk.level = registered_talk.level
    talk.abstract = registered_talk.abstract
    talk.category = registered_talk.category
    talk.knowledge = registered_talk.knowledge
    talk.notes = registered_talk.notes
    talk.put()
    return True


def user_is_attendee(user):
    """Check if the current user is already registered as an attendee."""
    attendee = model.Attendee.all()
    attendee.filter('userId =', user)
    if attendee.count() != 0:
        return True
    return False


def get_attendees():
    attendees = model.Attendee.all()
    return attendees


def get_profile(user):
    attendee = model.Attendee.all()
    attendee.filter('userId =', user)
    if attendee.count() == 0:
        return None
    return attendee[0]


def get_user_talks(user):
    talks = model.Talk.all()
    talks.filter('userId =', user)
    if talks.count() == 0:
        return None
    return talks


def get_talk(user, key):
    talks = model.Talk.all()
    talks.filter('userId =', user)
    if talks.count() == 0:
        return None
    for talk in talks:
        if str(talk.key()) == key:
            return talk
