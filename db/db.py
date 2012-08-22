# -*- coding: utf-8 *-*

import model


def check_attendee_exists(userid, profile):
    exist = model.Attendee.all()
    exist.filter('userId =', userid)
    if userid is not None and exist.count() != 0:
        return True, exist
    exist = model.Attendee.all()
    exist.filter('profile =', profile)
    if profile is not None and exist.count() != 0:
        return True, exist
    return False, ()


def user_talks(userid, profile):
    talks = model.Talk.all()
    talks.filter('userId =', userid)
    if userid is not None and talks.count() != 0:
        return True, talks
    talks = model.Talk.all()
    talks.filter('profile =', profile)
    if profile is not None and talks.count() != 0:
        return True, talks
    return False, ()


def check_tshirts(userid, profile):
    exist = model.Tshirt.all()
    exist.filter('userId =', userid)
    if userid is not None and exist.count() != 0:
        return True, exist
    exist = model.Tshirt.all()
    exist.filter('profile =', profile)
    if profile is not None and exist.count() != 0:
        return True, exist
    return False, ()


def add_attendee(attendee):
    """Register a new attendee in the database."""
    # Check if this user is already registered
    exists = check_attendee_exists(attendee.userId, attendee.profile)
    if exists[0]:
        return False

    if (attendee.personal_page and
       not attendee.personal_page.startswith('http://')):
        attendee.personal_page = 'http://%s' % attendee.personal_page
    if (attendee.company_page and
       not attendee.company_page.startswith('http://')):
        attendee.company_page = 'http://%s' % attendee.company_page

    attendee.put()
    return True


def request_tshirt(tshirt):
    exists = check_tshirts(tshirt.userId, tshirt.profile)
    if exists[0]:
        temp = exists[1][0]
        temp.color = tshirt.color
        temp.size = tshirt.size
        temp.total = tshirt.total
        temp.model = tshirt.model
        tshirt = temp

    tshirt.put()
    return True


def update_attendee(registered_attendee):
    """Register a new attendee in the database."""
    # Check that this user is already registered
    exists = check_attendee_exists(
        registered_attendee.userId, registered_attendee.profile)
    if not exists[0]:
        return False

    attendee = exists[1][0]
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
    exists = check_attendee_exists(talk.userId, talk.profile)
    if not exists[0]:
        return False

    talk.put()
    return True


def update_talk(key, registered_talk):
    """Register a new talk for the event."""
    # Check if this user is already registered
    found, talks = user_talks(registered_talk.userId, registered_talk.profile)
    if not found:
        return False

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
    exists = check_attendee_exists(user, user)
    if exists[0]:
        return True
    return False


def get_attendees():
    attendees = model.Attendee.all()
    return attendees


def get_profile(user):
    exists = check_attendee_exists(user, user)
    if exists[0]:
        return exists[1][0]


def get_user_talks(user):
    found, talks = user_talks(user, user)
    if not found:
        return None
    return talks


def get_talk(user, key):
    found, talks = user_talks(user, user)
    if not found:
        return None
    for talk in talks:
        if str(talk.key()) == key:
            return talk


def get_tshirts_requested(user):
    found, tshirts = check_tshirts(user, user)
    if not found:
        return None
    return tshirts[0]
