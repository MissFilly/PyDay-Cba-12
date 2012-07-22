# -*- coding: utf-8 *-*
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


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


class About(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),
            "templates/conference/about.html")
        self.response.out.write(template.render(path, {}))

class Attendees(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), "templates/others/attendees.html")
        self.response.out.write(template.render(path, {}))

def main():
    application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/register', Register),
        ('/about', About),
	('/attendees', Attendees),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
