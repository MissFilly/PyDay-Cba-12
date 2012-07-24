# -*- coding: utf-8 *-*
import os
import cgi

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from db import db


providers = {
    'Google': 'www.google.com/accounts/o8/id',
    'Yahoo': 'yahoo.com',
    'MySpace': 'myspace.com',
    'AOL': 'aol.com',
    'MyOpenID': 'myopenid.com',
    'LinkedIn': 'linkedin.com',
    'Twitter': 'twitter.com',
    'Facebook': 'facebook.com'
    # add more here
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
#            for name, uri in providers.items():
#                self.result.out.write('[<a href="%s">%s</a>]' % (
#                    users.create_login_url(federated_identity=uri), name))

        return result

    def show_openid_login(self):
        data = {}
        for name, uri in providers.items():
            data[name] = users.create_login_url(federated_identity=uri)
        path = os.path.join(os.path.dirname(__file__),
            "templates/others/login.html")
        self.response.out.write(template.render(path, data))

    def go_to_login(self, data):
        path = os.path.join(os.path.dirname(__file__),
            "templates/others/login.html")
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
                self.show_error(
                    u'Falta completar alguno de los datos requeridos.', data)
                return

            registered = db.add_attendee(result['user'], name, surname, nick,
                email, level, country, state, tel, in_attendees, allow_contact,
                personal_page, company, company_page, biography, cv)
            if registered:
                pass
            else:
                self.show_error(
                u'Hubo un problema al intentar procesar la inscripción.', data)
                # show error
        else:
            #show error page
            self.show_error(
                u'No hay una sesión iniciada.', data)

    def show_error(self, message, data):
        data['showerror'] = 'block'
        data['errormessage'] = message
        path = os.path.join(os.path.dirname(__file__),
            "templates/user/register.html")
        self.response.out.write(template.render(path, data))


class Propose(PyDayHandler):
    def get(self):
        user = users.get_current_user()
        registered = db.user_is_attendee(user)
        if not registered:
            self.redirect('/register')
            return
        if user:
            data = {'username': user.nickname(),
                'logout': users.create_logout_url(self.request.uri)}
            path = os.path.join(os.path.dirname(__file__),
                "templates/others/propose.html")
            self.response.out.write(template.render(path, data))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user = users.get_current_user()
        if user:
            self.response.out.write('<html><body>You wrote:<pre>')
            title = cgi.escape(self.request.get('title'))
            level = cgi.escape(self.request.get('talk-level'))
            abstract = cgi.escape(self.request.get('abstract'))
            category = cgi.escape(self.request.get('talk-category'))
            knowledge = cgi.escape(self.request.get('req-knowledge'))
            notes = cgi.escape(self.request.get('notes'))

            if not (title and abstract):
                #error page
                return

            saved = db.add_talk(user, title, level, abstract, category,
                knowledge, notes)
            if saved:
                self.response.out.write(repr(title) + '\n')
                self.response.out.write(repr(level) + '\n')
                self.response.out.write(repr(abstract) + '\n')
                self.response.out.write(repr(category) + '\n')
                self.response.out.write(repr(knowledge) + '\n')
                self.response.out.write(repr(notes) + '\n')
                self.response.out.write('</pre></body></html>')
        else:
            #show error page
            pass


class About(PyDayHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            data = {'username': user.nickname(),
                'logout': users.create_logout_url(self.request.uri)}
        else:
            data = {'login': users.create_login_url(self.request.uri)}
        path = os.path.join(os.path.dirname(__file__),
            "templates/conference/about.html")
        self.response.out.write(template.render(path, data))


class Venue(PyDayHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            data = {'username': user.nickname(),
                'logout': users.create_logout_url(self.request.uri)}
        else:
            data = {'login': users.create_login_url(self.request.uri)}
        path = os.path.join(os.path.dirname(__file__),
            "templates/conference/venue.html")
        self.response.out.write(template.render(path, data))


class Attendees(PyDayHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            data = {'username': user.nickname(),
                'logout': users.create_logout_url(self.request.uri)}
        else:
            data = {'login': users.create_login_url(self.request.uri)}
        attendees = db.get_attendees()
        len_attendees = attendees.count()
        attendees.filter('in_attendees =', True)
        data['attendees'] = attendees
        data['len_attendees'] = len_attendees
        path = os.path.join(os.path.dirname(__file__),
            "templates/others/attendees.html")
        self.response.out.write(template.render(path, data))


class Login(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            data = {'username': user.nickname(),
                'logout': users.create_logout_url(self.request.uri)}
        else:
            data = {'login': users.create_login_url(self.request.uri)}
        attendees = db.get_attendees()
        len_attendees = attendees.count()
        attendees.filter('in_attendees =', True)
        data['attendees'] = attendees
        data['len_attendees'] = len_attendees
        path = os.path.join(os.path.dirname(__file__),
            "templates/others/login.html")
        self.response.out.write(template.render(path, data))


def main():
    application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/register', Register),
        ('/about', About),
        ('/attendees', Attendees),
        ('/venue', Venue),
        ('/propose', Propose),
        ('/login', Login),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
