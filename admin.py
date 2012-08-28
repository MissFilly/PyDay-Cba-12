# -*- coding: utf-8 *-*
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import pyday
from db import model


class Talks(pyday.PyDayHandler):
    def get(self):
        talks = model.Talk.all()
        result = self.user_login()
        result['talks'] = talks
        path = os.path.join(os.path.dirname(__file__),
            "templates/admin/talks.html")
        self.response.out.write(template.render(path, result))


class Mails(pyday.PyDayHandler):
    def get(self):
        mails = model.Attendee.all()
        result = self.user_login()
        emails = 'contacto@pydaycba.com.ar'
        for user in mails:
            email = user.email
            if '@' not in email:
                email = '%s@gmail.com' % email
            emails = '%s, %s' % (emails, email)
        result['mails'] = emails
        path = os.path.join(os.path.dirname(__file__),
            "templates/admin/mails.html")

        self.response.out.write(template.render(path, result))


def main():
    application = webapp.WSGIApplication([
        ('/talks', Talks),
        ('/mails', Mails),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
