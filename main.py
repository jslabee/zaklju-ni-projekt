#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users
from models import Message
import json
from google.appengine.api import urlfetch


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logiran = True


            logout_url = users.create_logout_url('/')

            params = {"logiran": logiran, "logout_url": logout_url, "user": user}

            return self.render_template("vstopna.html", params)
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url, "user": user}
            return self.render_template("hello.html", params)

class VstopniHandler(BaseHandler):
    def post(self):
        return self.render_template("vstopna.html")



class MessageHandler(BaseHandler):

    def get(self):
        return self.render_template("message.html")

    def post(self):
        user = users.get_current_user()
        uporabnik_poslano= users.get_current_user()
        prejemnik = self.request.get("prejemnik")
        rezultat = self.request.get("vnos")


        message = Message(vnos=rezultat, uporabnik_poslano=user.nickname(),prejemnik=prejemnik)
        message.put()
        return self.write(rezultat)





class PrejetoHandler(BaseHandler):
    def get(self):

        user = users.get_current_user()
        seznam = Message.query(Message.prejemnik == user.nickname()).fetch()

        params = {"seznam": seznam}

        return self.render_template("prejeto.html", params)

class PoslanoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        seznam = Message.query(Message.uporabnik_poslano == user.nickname()).fetch()

        params = {"seznam": seznam}

        return self.render_template("poslano.html", params)



class  VremeHandler(BaseHandler):
    def get(self):
        url = "http://api.openweathermap.org/data/2.5/weather?q=Brasilia,br&units=metric&appid=a3306fa6e0273fbd2c0a9e5bc1dcdd98"

        result = urlfetch.fetch(url)

        podatki = json.loads(result.content)

        params = {"podatki": podatki}

        return self.render_template("vreme.html", params)








app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vstopna', VstopniHandler),
    webapp2.Route('/message', MessageHandler),
    webapp2.Route('/rezultat', MessageHandler),
    webapp2.Route('/poslano', PoslanoHandler),
    webapp2.Route('/prejeto', PrejetoHandler),
    webapp2.Route('/vreme', VremeHandler),
], debug=True)
