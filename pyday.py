# -*- coding: utf-8 *-*
import os
import cgi

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from db import db


providers = {
    'google': 'www.google.com/accounts/o8/id',
    'yahoo': 'yahoo.com',
    'live': 'myspace',
    'aol': 'aol.com',
    'openid': 'myopenid.com',
}


class PyDayHandler(webapp.RequestHandler):
    def user_login(self):
        result = {}
        user = users.get_current_user()
        if user:  # signed in already
            result['user'] = user
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
        path = os.path.join(os.path.dirname(__file__), page_base)
        self.response.out.write(template.render(path, data))


class MainPage(PyDayHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__), "templates/index.html")
        self.response.out.write(template.render(path, result))


class Register(PyDayHandler):
    def get(self):
        result = self.user_login()
        if result.get('user', None):
            result['showerror'] = 'none'
            path = os.path.join(os.path.dirname(__file__),
                "templates/user/register.html")
            self.response.out.write(template.render(path, result))
        else:
            self.go_to_login(result)

    def post(self):
        result = self.user_login()
        # Collect data
        name = cgi.escape(self.request.get('name'))
        surname = cgi.escape(self.request.get('last-name'))
        nick = cgi.escape(self.request.get('nick'))
        email = cgi.escape(self.request.get('email'))
        level = cgi.escape(self.request.get('level'))
        country = cgi.escape(self.request.get('country'))
        state = cgi.escape(self.request.get('state'))
        tel = cgi.escape(self.request.get('tel'))
        in_attendees = cgi.escape(self.request.get('include-attendees'))
        allow_contact = cgi.escape(self.request.get('sponsors-contact'))
        personal_page = cgi.escape(self.request.get('personal-page'))
        company = cgi.escape(self.request.get('company'))
        company_page = cgi.escape(self.request.get('company-page'))
        biography = cgi.escape(self.request.get('biography'))
        cv = cgi.escape(self.request.get('cv'))
        data = {
            'name': name,
            'surname': surname,
            'nick': nick,
            'email': email,
            'tel': tel,
            'personal_page': personal_page,
            'company': company,
            'company_page': company_page,
            'biography': biography,
        }
        data.update(result)

        if result.get('user', None):
            if not (name and surname and email):
                #error page
                self.show_error("templates/user/register.html",
                    u'Falta completar alguno de los datos requeridos.', data)
                return

            registered = db.add_attendee(result['user'], name, surname, nick,
                email, level, country, state, tel, in_attendees, allow_contact,
                personal_page, company, company_page, biography, cv)
            if registered:
                data['title'] = (
                    u'Te registraste exitosamente en el PyDay Córdoba 2012.')
                data['message'] = (
                    u'Podés ver <a href="/attendees">quiénes van'
                    ' a asistir</a> o compartirlo en:')
                data['share_twitter'] = (
                    u'https://twitter.com/intent/tweet?text=Voy+a+asistir '
                    'al+%23PyDayCba+el+15+de+septiembre+-+'
                    u'http://pydaycba.com.ar+¡Inscribite+vos+también!')
                data['share_facebook'] = (
                    u'http://www.facebook.com/sharer/sharer.php?'
                    u'u=http://pydaycba.com.ar/')
                path = os.path.join(os.path.dirname(__file__),
                    "templates/user/success.html")
                self.response.out.write(template.render(path, data))
            else:
                self.show_error("templates/user/register.html",
                u'Hubo un problema al intentar procesar la inscripción.', data)
                # show error
        else:
            #show error page
            self.show_error("templates/user/register.html",
                u'No hay una sesión iniciada.', data)


class Propose(PyDayHandler):
    def get(self):
        result = self.user_login()
        registered = db.user_is_attendee(result.get('user', None))
        if not registered:
            self.redirect('/register')
            return
        if result.get('user', None):
            path = os.path.join(os.path.dirname(__file__),
                "templates/others/propose.html")
            self.response.out.write(template.render(path, result))
        else:
            self.redirect(result['login'])

    def post(self):
        result = self.user_login()
        # Collect data
        title = cgi.escape(self.request.get('title'))
        level = cgi.escape(self.request.get('talk-level'))
        abstract = cgi.escape(self.request.get('abstract'))
        category = cgi.escape(self.request.get('talk-category'))
        knowledge = cgi.escape(self.request.get('req-knowledge'))
        notes = cgi.escape(self.request.get('notes'))
        data = {
            'title': title,
            'abstract': abstract,
            'knowledge': knowledge,
            'notes': notes,
        }
        data.update(result)
        if result.get('user', None):

            if not (title and abstract):
                #error page
                self.show_error("templates/others/propose.html",
                    u'Falta completar alguno de los datos requeridos.', data)
                return

            saved = db.add_talk(result['user'], title, level, abstract,
                category, knowledge, notes)
            if saved:
                data['title'] = u'Tu propuesta fue cargada con éxito.'
                data['message'] = u'Podés compartirlo en:'
                data['share_twitter'] = (
                    u'https://twitter.com/intent/tweet?text=Propuse la charla+'
                    u'%s+para+el+%23PyDayCba+-+http://pydaycba.com.ar ¡Sumate!' %
                    title)
                data['share_facebook'] = (
                    u'http://www.facebook.com/sharer/sharer.php?'
                    u'u=http://pydaycba.com.ar/')
                path = os.path.join(os.path.dirname(__file__),
                    "templates/user/success.html")
                self.response.out.write(template.render(path, data))
        else:
            #show error page
            self.show_error("templates/others/propose.html",
                u'Hubo un problema al intentar registrar la charla.', data)


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
            }
            result.update(data)
            talks = db.get_user_talks(result['user'])
            if talks:
                result['talks'] = talks
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


class Success(PyDayHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__),
            "templates/user/success.html")
        self.response.out.write(template.render(path, result))


class ModifyProfile(PyDayHandler):
    def get(self):
        result = self.user_login()
        if result.get('user', None):
            attendee = db.get_profile(result['user'])
            if attendee is None:
                self.redirect('/register')
                return
            data = {
                'name': attendee.name,
                'surname': attendee.surname,
                'nick': attendee.nick,
                'email': attendee.email,
                'tel': attendee.tel,
                'personal_page': attendee.personal_page,
                'company': attendee.company,
                'company_page': attendee.company_page,
                'biography': attendee.biography,
            }
            result.update(data)
        path = os.path.join(os.path.dirname(__file__),
            "templates/user/register.html")
        self.response.out.write(template.render(path, result))

    def post(self):
        result = self.user_login()
        # Collect data
        name = cgi.escape(self.request.get('name'))
        surname = cgi.escape(self.request.get('last-name'))
        nick = cgi.escape(self.request.get('nick'))
        email = cgi.escape(self.request.get('email'))
        level = cgi.escape(self.request.get('level'))
        country = cgi.escape(self.request.get('country'))
        state = cgi.escape(self.request.get('state'))
        tel = cgi.escape(self.request.get('tel'))
        in_attendees = cgi.escape(self.request.get('include-attendees'))
        allow_contact = cgi.escape(self.request.get('sponsors-contact'))
        personal_page = cgi.escape(self.request.get('personal-page'))
        company = cgi.escape(self.request.get('company'))
        company_page = cgi.escape(self.request.get('company-page'))
        biography = cgi.escape(self.request.get('biography'))
        cv = cgi.escape(self.request.get('cv'))
        data = {
            'name': name,
            'surname': surname,
            'nick': nick,
            'email': email,
            'tel': tel,
            'personal_page': personal_page,
            'company': company,
            'company_page': company_page,
            'biography': biography,
        }
        data.update(result)

        if result.get('user', None):
            if not (name and surname and email):
                #error page
                self.show_error("templates/user/register.html",
                    u'Falta completar alguno de los datos requeridos.', data)
                return

            registered = db.update_attendee(result['user'], name, surname,
                nick, email, level, country, state, tel, in_attendees,
                allow_contact, personal_page, company, company_page, biography,
                cv)
            if registered:
                data['title'] = (
                    u'Registración actualizada exitosamente para'
                    u' el PyDay Córdoba 2012.')
                data['message'] = (
                    u'Podés ver <a href="/attendees">quiénes van'
                    ' a asistir</a> o compartirlo en:')
                data['share_twitter'] = (
                    u'https://twitter.com/intent/tweet?text=Voy+a+asistir'
                    '+al+%23PyDayCba+el+15+de+septiembre+-+'
                    u'http://pydaycba.com.ar+¡Inscribite+vos+también!')
                data['share_facebook'] = (
                    u'http://www.facebook.com/sharer/sharer.php?'
                    u'u=http://pydaycba.com.ar/')
                path = os.path.join(os.path.dirname(__file__),
                    "templates/user/success.html")
                self.response.out.write(template.render(path, data))
            else:
                self.show_error("templates/user/register.html",
                u'Hubo un problema al intentar procesar la inscripción.', data)
                # show error
        else:
            #show error page
            self.show_error("templates/user/register.html",
                u'No hay una sesión iniciada.', data)


class ModifyTalk(PyDayHandler):
    def get(self):
        result = self.user_login()
        cv = cgi.escape(self.request.get('algo'))
        self.response.out.write(cv)
#        registered = db.user_is_attendee(result.get('user', None))
#        if not registered:
#            self.redirect('/register')
#            return
#        if result.get('user', None):
#            talks = db.get_user_talks(result['user'])
#            path = os.path.join(os.path.dirname(__file__),
#                "templates/others/propose.html")
#            self.response.out.write(template.render(path, result))
#        else:
#            self.redirect(result['login'])


def main():
    application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/register', Register),
        ('/about', About),
        ('/profile', Profile),
        ('/attendees', Attendees),
        ('/venue', Venue),
        ('/propose', Propose),
        ('/success', Success),
        ('/login', Login),
        ('/modify_profile', ModifyProfile),
        ('/modify_talk', ModifyTalk),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
