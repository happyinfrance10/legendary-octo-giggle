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
    level = ndb.IntegerProperty()
    #determines where the question is in the sequence, e.g. 1 in a 10-question sequence

class Sequence(ndb.Model):
    name = ndb.StringProperty()
    questions = ndb.StructuredProperty(Question, repeated=True)
    #defines the question property as a list of questions
    description = ndb.StringProperty()
    rating = ndb.FloatProperty()
    difficulty = ndb.FloatProperty()

question1 = Question(
    question = '1010100, nzccfn, 7DB',
    answer = 'Sun Microsystems',
    level = 1
)

sequenceA = Sequence(
    name = "Tech Companies"
    questions = [question1],
    description = "Learn about the tech companies of the world!",
    rating = 5.00,
    difficulty = 5.00,
)

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
# Which one are we using????
class LevelPage(webapp2.RequestHandler):
    def get(self):
        question = self.request.get("question")
        answer = self.request.get("answer")
        template = env.get_template("templates/level1.html")
        templateVars = {
            "question" : question,
            "answer" : answer,
        }
        self.response.write(template.render(templateVars))

class Level(webapp2.RequestHandler) :
    def get(self) :
        template = env.get_template("templates/level.html")
        self.response.write(template.render())
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
    ("/levelpage", LevelPage),
    ("/level", Level),
    # ("/sequence", SequencePage),
    # ("/upload_photo", PhotoUploadHandler),
    # ("/photo", PhotoHandler),
], debug=True)
