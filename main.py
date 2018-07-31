import webapp2
import jinja2
import os
import datetime
import logging
import time

#may want to use PIL images for uploading images
from google.appengine.api import users
from google.appengine.ext import ndb

env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class Person(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    level = ndb.StringProperty()

class Question(ndb.Model):
    question = ndb.StringProperty()
    answer = ndb.StringProperty()
    location = ndb.StringProperty()

class Level(ndb.Model):
    levelnumber = ndb.IntegerProperty()
    question_key = ndb.KeyProperty()

class Sequence(ndb.Model):
    pass

class MainPage(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        people = Person.query().fetch()
        if current_user:
            current_email = current_user.email()
            current_person = Person.query().filter(Person.email == current_email).get()
        else:
            current_person = None

        logout_url = users.create_logout_url("/")
        login_url = users.create_login_url("/")

        templateVars = {
            "people" : people,
            "current_user" : current_user,
            "login_url" : login_url,
            "logout_url" : logout_url,
            "current_person" : current_person,
        }
        # current_user = users.get_current_user()
        #if no one is logged in, show a login prompt.
        # logout_url = users.create_logout_url('/')
        # login_url = users.create_login_url('/')
        # people = Person.query().fetch()
        # if current_user:
        #     current_email = current_user.email()
        #     current_person=Person.query().filter(Person.email==current_email).get()
        # else:
        #     current_person = None
            # 'login_url': login_url,
            # 'logout_url': logout_url,
        template = env.get_template("templates/home.html")
        self.response.write(template.render(templateVars))

class LevelPage(webapp2.RequestHandler):
    def get(self):
        # levels = Level.query().filter(Level.levelnumber == 1).fetch()
        # for level in levels:
        #     question = Question.query().filter(Question.key == level.question_key).get()
        question = 'Question' #temporary value for testing
        template = env.get_template("templates/level.html")
        templateVars = {
            "question" : question,
        }
        self.response.write(template.render(templateVars))


    # def post(self):
    #     content=self.request.get('content')
    #     current_user = users.get_current_user()
    #     email = current_user.email()
    #
    #     message = Message(email=email, content=content)
    #     message.put()
    #
    #     time.sleep(1)
    #     self.redirect('/')

# class ProfilePage(webapp2.RequestHandler):
#     def get(self):
#         urlsafe_key = self.request.get('key')
#         current_user = users.get_current_user()
#         key = ndb.Key(urlsafe=urlsafe_key)
#         person=key.get()
#
#         is_my_profile = current_user and current_user.email()==person.email
#         templateVars = {
#             'person' : person,
#             'is_my_profile': is_my_profile,
#             # 'current_user': current_user,
#             # 'login_url': login_url,
#         }
#         template = env.get_template("templates/profile.html")
#         self.response.write(template.render(templateVars))

# class CreateHandler(webapp2.RequestHandler):
#     def post(self):
#         # 1. get info from the request
#         name = self.request.get('name')
#         biography = self.request.get('biography')
#         current_user = users.get_current_user()
#         email = current_user.email()
#         # 2. read or write to the database
#         person = Person(name=name, biography=biography, email=email)
#         person.put()
#         # 3. render a response
#         time.sleep(1)
#         self.redirect('/')

# class PhotoUploadHandler(webapp2.RequestHandler):
#     def post(self):
#         # # 1. get info from the request
#         # image = self.request.get('image')
#         # # biography = self.request.get('biography')
#         # current_user = users.get_current_user()
#         # current_person=Person.query().filter(Person.email==current_user.email()).get()
#         # current_person.photo = image
#         # current_person.put()
#         # # email = current_user.email()
#         # # # 2. read or write to the database
#         # # person = Person(name=name, biography=biography, email=email)
#         # # person.put()
#         # # # 3. render a response
#         # time.sleep(1)
#         # self.redirect('/profile?key='+current_person.key.urlsafe())
#
# class PhotoHandler(webapp2.RequestHandler):
#     def get(self):
        # urlsafe_key=self.request.get('key')
        # key = ndb.Key(urlsafe=urlsafe_key)
        # person=key.get()
        # self.response.headers['Content-Type'] = 'image/jpeg'
        # self.response.write(person.photo)

app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/level", LevelPage)
    # ("/sequence", SequencePage),
    # ("/upload_photo", PhotoUploadHandler),
    # ("/photo", PhotoHandler),
], debug=True)
