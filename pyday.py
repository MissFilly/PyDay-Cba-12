# -*- coding: utf-8 *-*
import os
import cgi

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from db import db


class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), "templates/index.html")
        self.response.out.write(template.render(path, {}))


class Register(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            path = os.path.join(os.path.dirname(__file__),
                "templates/user/register.html")
            self.response.out.write(template.render(path, {}))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user = users.get_current_user()
        if user:
            self.response.out.write('<html><body>You wrote:<pre>')
            name = cgi.escape(self.request.get('name'))
            surname = cgi.escape(self.request.get('last-name'))
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

            db.add_attendee(user, name, surname, email, level, country, state,
                tel, in_attendees, allow_contact, personal_page, company,
                company_page, biography, cv)
            self.response.out.write(name + '\n')
            self.response.out.write(surname + '\n')
            self.response.out.write(email + '\n')
            self.response.out.write(level + '\n')
            self.response.out.write(country + '\n')
            self.response.out.write(state + '\n')
            self.response.out.write(tel + '\n')
            self.response.out.write(repr(in_attendees) + '\n')
            self.response.out.write(repr(allow_contact) + '\n')
            self.response.out.write(personal_page + '\n')
            self.response.out.write(company + '\n')
            self.response.out.write(company_page + '\n')
            self.response.out.write(biography + '\n')
            self.response.out.write(repr(cv) + '\n')
            self.response.out.write('DIEGOOOOOOOOOOO')
            self.response.out.write('</pre></body></html>')
        else:
            #show error page
            pass


class About(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),
            "templates/conference/about.html")
        self.response.out.write(template.render(path, {}))


def main():
    application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/register', Register),
        ('/about', About),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
