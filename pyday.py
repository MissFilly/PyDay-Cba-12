# -*- coding: utf-8 *-*
import os
import cgi

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import forms
import utils
from db import db
from db.model import TwitterProfile
from gaesessions import get_current_session


MESSAGE_REGISTER = (u'Voy a asistir al %23PyDayCba el 15 de septiembre - '
                    u'http://pydaycba.com.ar ¡Inscribite vos también!')
MESSAGE_PROPOSE = (u'Propuse la charla %s para el %%23PyDayCba - '
                   u'http://pydaycba.com.ar ¡Sumate!')
FACEBOOK_MESSAGE = (u'http://www.facebook.com/sharer/sharer.php?'
                    u'u=http://pydaycba.com.ar/')


providers = {
    'google': 'www.google.com/accounts/o8/id',
    'yahoo': 'yahoo.com',
    'aol': 'aol.com',
    'openid': 'myopenid.com',
}


def get_twitter_message(message):
    return (u'https://twitter.com/intent/tweet?text=%s' %
        message.replace(' ', '+'))


class PyDayHandler(webapp.RequestHandler):

    def user_login(self):
        result = {}
        user = users.get_current_user()
        is_profile = False
        if user is None:
            session = get_current_session()
            twitter_user = session.get("twitter_user")
            if twitter_user is not None:
                user = TwitterProfile.get_by_key_name(twitter_user)
                is_profile = True

        message = utils.days_left_message()
        result['daysleft0'] = message[0]
        result['daysleft1'] = message[1]
        result['daysleft2'] = message[2]
        if user:  # signed in already
            result['user'] = user
            if is_profile:
                result['logout'] = '/oauth/signout'
            else:
                result['logout'] = users.create_logout_url(self.request.uri)
            result['username'] = user.nickname()
        else:  # let user choose authenticator
            result['user'] = None
            result['login'] = '/login'

        return result

    def go_to_login(self, data):
        for name, uri in providers.items():
            data[name] = users.create_login_url(federated_identity=uri)
        path = os.path.join(os.path.dirname(__file__),
            "templates/others/login.html")
        self.response.out.write(template.render(path, data))

    def show_error(self, page_base, message, data):
        data['showerror'] = 'block'
        data['errormessage'] = message
        if 'form' in data:
            data['form'].errors.clear()
        path = os.path.join(os.path.dirname(__file__), page_base)
        self.response.out.write(template.render(path, data))

class NotFoundPageHandler(PyDayHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__),
            "templates/others/404.html")
        self.response.out.write(template.render(path, result))


class MainPage(PyDayHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__), "templates/index.html")
        self.response.out.write(template.render(path, result))


class Schedule(PyDayHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__),
            "templates/conference/schedule.html")
        self.response.out.write(template.render(path, result))


class Register(PyDayHandler):
    def get(self):
        result = self.user_login()
        if result.get('user', None):
            result['showerror'] = 'none'
            result['register_selected'] = 'class="active"'
            form = forms.AttendeeForm()
            form.initial = {'allow_contact': True,
                'in_attendees': True}
            result['form'] = form
            path = os.path.join(os.path.dirname(__file__),
                "templates/user/register.html")
            self.response.out.write(template.render(path, result))
        else:
            self.go_to_login(result)

    def post(self):
        result = self.user_login()
        values = forms.AttendeeForm(data=self.request.POST)
        result['form'] = values

        if result.get('user', None):
            if not values.is_valid():
                #error page
                self.show_error("templates/user/register.html",
                    u'Falta completar alguno de los datos requeridos.', result)
                return

            attendee = values.save(commit=False)
            user = result['user']
            if isinstance(user, users.User):
                attendee.userId = result['user']
            else:
                attendee.profile = result['user']
            registered = db.add_attendee(attendee)
            if registered:
                data = {}
                data['title'] = (
                    u'Te registraste exitosamente en el PyDay Córdoba 2012.')
                data['message'] = (
                    u'Podés ver <a href="/attendees">quiénes van'
                    ' a asistir</a> o compartirlo en:')
                data['share_twitter'] = get_twitter_message(MESSAGE_REGISTER)
                data['share_facebook'] = FACEBOOK_MESSAGE
                data.update(result)
                path = os.path.join(os.path.dirname(__file__),
                    "templates/user/success.html")
                self.response.out.write(template.render(path, data))
            else:
                self.show_error("templates/user/register.html",
                u'Hubo un problema al intentar procesar la inscripción '
                u'o el usuario ingresado ya existe.',
                    result)
                # show error
        else:
            #show error page
            self.show_error("templates/user/register.html",
                u'No hay una sesión iniciada.', result)


class Propose(PyDayHandler):
    def get(self):
        result = self.user_login()
        registered = db.user_is_attendee(result.get('user', None))
        if not registered:
            self.redirect('/register')
            return
        if result.get('user', None):
            form = forms.TalkForm()
            result['form'] = form
            result['propose_selected'] = 'class="active"'
            path = os.path.join(os.path.dirname(__file__),
                "templates/others/propose.html")
            self.response.out.write(template.render(path, result))
        else:
            self.redirect(result['login'])

    def post(self):
        result = self.user_login()
        # Collect data
        values = forms.TalkForm(data=self.request.POST)
        result['form'] = values

        if result.get('user', None):

            if not values.is_valid():
                #error page
                self.show_error("templates/others/propose.html",
                    u'Falta completar alguno de los datos requeridos.', result)
                return

            talk = values.save(commit=False)
            user = result['user']
            if isinstance(user, users.User):
                talk.userId = user
            else:
                talk.profile = user
            saved = db.add_talk(talk)
            if saved:
                data = {}
                data['title'] = u'Tu propuesta fue cargada con éxito.'
                data['message'] = u'Podés compartirlo en:'
                data['share_twitter'] = get_twitter_message(
                    MESSAGE_PROPOSE % talk.title)
                data['share_facebook'] = FACEBOOK_MESSAGE
                data.update(result)
                path = os.path.join(os.path.dirname(__file__),
                    "templates/user/success.html")
                self.response.out.write(template.render(path, data))
            else:
                #show error page
                self.show_error("templates/others/propose.html",
                  u'Hubo un problema al intentar registrar la charla.', result)
        else:
            #show error page
            self.show_error("templates/others/propose.html",
                u'Hubo un problema al intentar registrar la charla.', result)


class About(PyDayHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__),
            "templates/conference/about.html")
        self.response.out.write(template.render(path, result))


class Venue(PyDayHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__),
            "templates/conference/venue.html")
        self.response.out.write(template.render(path, result))


class Attendees(PyDayHandler):
    def get(self):
        result = self.user_login()
        attendees = db.get_attendees()
        len_attendees = attendees.count()
        attendees.filter('in_attendees =', True)
        result['attendees'] = attendees
        result['len_attendees'] = len_attendees
        path = os.path.join(os.path.dirname(__file__),
            "templates/others/attendees.html")
        self.response.out.write(template.render(path, result))


class Profile(PyDayHandler):
    def get(self):
        result = self.user_login()
        if result.get('user', None):
            attendee = db.get_profile(result['user'])
            if attendee is None:
                self.redirect('/register')
                return
            in_attendees = u'Sí' if attendee.in_attendees else 'No'
            allow_contact = u'Sí' if attendee.allow_contact else 'No'
            assist_dinner = u'Sí' if attendee.assist_dinner else 'No'
            data = {
                'name': attendee.name,
                'surname': attendee.surname,
                'nick': attendee.nick,
                'email': attendee.email,
                'level': attendee.level,
                'country': attendee.country,
                'state': attendee.state,
                'tel': attendee.tel,
                'personal_page': attendee.personal_page,
                'company': attendee.company,
                'company_page': attendee.company_page,
                'in_attendees': in_attendees,
                'allow_contact': allow_contact,
                'biography': attendee.biography,
                'assist_dinner': assist_dinner,
            }
            if attendee.cv:
                data['cv'] = attendee.cv
            result.update(data)
            talks = db.get_user_talks(result['user'])
            if talks:
                result['talks'] = talks
            tshirt = db.get_tshirts_requested(result['user'])
            if tshirt:
                result['tshirt'] = tshirt
            path = os.path.join(os.path.dirname(__file__),
                "templates/user/profile.html")
            self.response.out.write(template.render(path, result))
        else:
            self.redirect('/register')


class Login(PyDayHandler):
    def get(self):
        result = self.user_login()
        if result.get('user', None):
            self.redirect('/')
            return
        self.go_to_login(result)


class ModifyProfile(PyDayHandler):
    def get(self):
        result = self.user_login()
        if result.get('user', None):
            attendee = db.get_profile(result['user'])
            if attendee is None:
                self.redirect('/register')
                return
            result['register_selected'] = 'class="active"'
            result['form'] = forms.AttendeeForm(instance=attendee)
        path = os.path.join(os.path.dirname(__file__),
            "templates/user/register.html")
        self.response.out.write(template.render(path, result))

    def post(self):
        result = self.user_login()
        values = forms.AttendeeForm(data=self.request.POST)
        result['form'] = values

        if result.get('user', None):
            if not values.is_valid():
                #error page
                self.show_error("templates/user/register.html",
                    u'Falta completar alguno de los datos requeridos.', result)
                return

            attendee = values.save(commit=False)
            user = result['user']
            if isinstance(user, users.User):
                attendee.userId = user
            else:
                attendee.profile = user
            registered = db.update_attendee(attendee)
            if registered:
                data = {}
                data['title'] = (
                    u'Registración actualizada exitosamente para'
                    u' el PyDay Córdoba 2012.')
                data['message'] = (
                    u'Podés ver <a href="/attendees">quiénes van'
                    ' a asistir</a> o compartirlo en:')
                data['share_twitter'] = get_twitter_message(MESSAGE_REGISTER)
                data['share_facebook'] = FACEBOOK_MESSAGE
                data.update(result)
                path = os.path.join(os.path.dirname(__file__),
                    "templates/user/success.html")
                self.response.out.write(template.render(path, data))
            else:
                self.show_error("templates/user/register.html",
                u'Hubo un problema al intentar procesar la inscripción.',
                result)
                # show error
        else:
            #show error page
            self.show_error("templates/user/register.html",
                u'No hay una sesión iniciada.', result)


class ModifyTalk(PyDayHandler):
    def get(self):
        result = self.user_login()
        key = cgi.escape(self.request.get('talk'))
        talk = db.get_talk(result['user'], key)
        if result.get('user', None) and talk:
            result['form'] = forms.TalkForm(instance=talk)
            result['propose_selected'] = 'class="active"'
            path = os.path.join(os.path.dirname(__file__),
                "templates/others/propose.html")
            self.response.out.write(template.render(path, result))
        else:
            self.redirect(result['login'])

    def post(self):
        result = self.user_login()
        # Collect data
        key = cgi.escape(self.request.get('talk'))
        values = forms.TalkForm(data=self.request.POST)
        result['form'] = values

        if result.get('user', None):

            if not values.is_valid():
                #error page
                self.show_error("templates/others/propose.html",
                    u'Falta completar alguno de los datos requeridos.', result)
                return

            talk = values.save(commit=False)
            user = result['user']
            if isinstance(user, users.User):
                talk.userId = user
            else:
                talk.profile = user
            saved = db.update_talk(key, talk)
            if saved:
                data = {}
                data['title'] = u'Tu propuesta fue cargada con éxito.'
                data['message'] = u'Podés compartirlo en:'
                data['share_twitter'] = get_twitter_message(
                    MESSAGE_PROPOSE % talk.title)
                data['share_facebook'] = FACEBOOK_MESSAGE
                data.update(result)
                path = os.path.join(os.path.dirname(__file__),
                    "templates/user/success.html")
                self.response.out.write(template.render(path, data))
        else:
            #show error page
            self.show_error("templates/others/propose.html",
                u'Hubo un problema al intentar registrar la charla.', result)


class Prospectus(PyDayHandler):
    def get(self):
        result = self.user_login()
        result['is_active'] = ' active'
        path = os.path.join(os.path.dirname(__file__),
            "templates/others/prospectus.html")
        self.response.out.write(template.render(path, result))


class Tshirt(PyDayHandler):
    def get(self):
        result = self.user_login()
        registered = db.user_is_attendee(result.get('user', None))
        if not registered:
            self.redirect('/register')
            return
        if result.get('user', None):
            form = forms.TshirtForm()
            result['form'] = form
            path = os.path.join(os.path.dirname(__file__),
                "templates/user/tshirt.html")
            self.response.out.write(template.render(path, result))
        else:
            self.redirect(result['login'])

    def post(self):
        result = self.user_login()
        # Collect data
        values = forms.TshirtForm(data=self.request.POST)
        result['form'] = values

        if result.get('user', None):
            if not values.is_valid():
                #error page
                self.show_error("templates/user/tshirt.html",
                    u'Falta completar alguno de los datos requeridos.', result)
                return

            tshirt = values.save(commit=False)
            user = result['user']
            if isinstance(user, users.User):
                tshirt.userId = user
            else:
                tshirt.profile = user
            saved = db.request_tshirt(tshirt)
            if saved:
                self.redirect('/profile')
            else:
                #show error page
                self.show_error("templates/user/tshirt.html",
                  u'Hubo un problema al intentar registrar la charla.', result)
        else:
            #show error page
            self.show_error("templates/user/tshirt.html",
                u'Hubo un problema al intentar registrar la charla.', result)


def main():
    application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/register', Register),
        ('/about', About),
        ('/profile', Profile),
        ('/attendees', Attendees),
        ('/venue', Venue),
        ('/propose', Propose),
        ('/login', Login),
        ('/modify_profile', ModifyProfile),
        ('/modify_talk', ModifyTalk),
        ('/prospectus', Prospectus),
        #('/tshirt', Tshirt),
        ('/schedule', Schedule),
        ('/.*', NotFoundPageHandler),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
