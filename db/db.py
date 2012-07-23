# -*- coding: utf-8 *-*

import model


def add_attendee(user, name, surname, nick, email, level, country, state, tel,
    in_attendees, allow_contact, personal_page, company, company_page,
    biography, cv):
    """Register a new attendee in the database."""
    # Check if this user is already registered
    attendee = model.Attendee.all()
    attendee.filter('userId =', user)
    if attendee.count() != 0:
        return False

    attendee = model.Attendee()
    attendee.userId = user
    attendee.name = name
    attendee.surname = surname
    attendee.nick = nick
    attendee.email = email
    attendee.level = level
    attendee.country = country
    attendee.state = state
    attendee.tel = tel
    attendee.in_attendees = True if in_attendees == 'on' else False
    attendee.allow_contact = True if allow_contact == 'on' else False
    if personal_page and not personal_page.startswith('http://'):
        personal_page = 'http://%s' % personal_page
    attendee.personal_page = personal_page
    attendee.company = company
    if company_page and not company_page.startswith('http://'):
        company_page = 'http://%s' % company_page
    attendee.company_page = company_page
    attendee.biography = biography
    attendee.cv = str(cv)

    attendee.put()
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
