from google.appengine.ext import ndb

class Message(ndb.Model):
    vnos = ndb.StringProperty()
    uporabnik_poslano= ndb.StringProperty()
    prejemnik = ndb.StringProperty()