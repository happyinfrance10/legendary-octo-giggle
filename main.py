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
    # current_level = ndb.IntegerProperty()

class Question(ndb.Model):
    sequence = ndb.StringProperty()
    question = ndb.StringProperty()
    answer = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    level_number = ndb.IntegerProperty()

class Level(ndb.Model): #keeps track of player progress per sequence
    player_key = ndb.KeyProperty()
    current_level = ndb.IntegerProperty()
    sequence = ndb.StringProperty()
    finished = ndb.BooleanProperty()

question1 = Question(sequence="1", question="1010100, nzccfn, 7DB", answer = "Sun Microsystems", location=ndb.GeoPt(0, 0), level_number=1)
question1.put()
question2 = Question(sequence="1", question="Hello, nzccfn, 7DB", answer = "Goodbye", location=ndb.GeoPt(0, 0), level_number=2)
question2.put()

class MainPage(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        people = Person.query().fetch()
        if current_user:
            current_email = current_user.email()
            current_person = Person.query().filter(Person.email == current_email).get()
        else:
            current_person = None

        # tracks progress of player within sequence 1
        if current_person:
            current_level_1 = Level.query().filter(Level.player_key == current_person.key).filter(Level.sequence == "1").get()
            # if the current user has no level progress, then create a new sequence
            if not current_level_1:
                # current_level_1 = Level(player_key = current_person.key, current_level=1, sequence="1")
                current_level_1 = Level(player_key = current_person.key, current_level=1, sequence="1", finished=False)
                current_level_1.put()
            # if the current user finished the level, then reset progress
            if (current_level_1.finished):
                current_level_1.finished = False
                current_level_1.current_level = 1
                current_level_1.put()

            # loads correct question from within sequence 1
            current_question_1 = Question.query().filter(Question.sequence == current_level_1.sequence).filter(Question.level_number == current_level_1.current_level).get()
            sequence1_key = current_question_1.key.urlsafe()
        else:
            sequence1_key = None
        logout_url = users.create_logout_url("/")
        login_url = users.create_login_url("/")

        templateVars = {
            "people" : people,
            "current_user" : current_user,
            "login_url" : login_url,
            "logout_url" : logout_url,
            "current_person" : current_person,
            "sequence1_key" : sequence1_key,
        }
        template = env.get_template("templates/home.html")
        self.response.write(template.render(templateVars))

class CreateHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get("name")
        current_user = users.get_current_user()
        email = current_user.email()
        #2 Read/write from database
        person = Person(name=name, email=email)
        person.put()
        time.sleep(2)
        self.redirect("/")

class LevelPage(webapp2.RequestHandler):
    def get(self):
        # load the level using the sequence and level_number given from the level object.

        # load the key for the next level in the sequence, based on the current user's progress.
        sequence_key = self.request.get('sequence') # for now sequence_key will display the sequence name
        urlsafe_key = self.request.get('key')
        key = ndb.Key(urlsafe=urlsafe_key)
        question=key.get()
        email = users.get_current_user().email()
        person = Person.query().filter(Person.email==email).get()
        current_level = Level.query().filter(Level.player_key == person.key).filter(Level.sequence == str(sequence_key)).get()

        answer_correct = self.request.get('answer_correct')
        # note to generalize to current sequence via the sequence_key next time.

        next_question = Question.query().filter(Question.sequence == str(sequence_key)).filter(Question.level_number == question.level_number+1).get()

        if (answer_correct):
            current_level.current_level = question.level_number
            current_level.put()

        # use that same current_level (after increase) and the sequence name to filter for a question within
        # the question database
        if(next_question):
            next_question_key = next_question.key.urlsafe()
        else:
            next_question_key = "null"
        # fetch that question, and return that key and pass as a template variable.
        template = env.get_template("templates/level.html")
        templateVars = {
            "question" : question,
            "next_question_key" : next_question_key,
            "sequence_key": sequence_key,
        }
        self.response.write(template.render(templateVars))

class AboutPage(webapp2.RequestHandler) :
    def get(self) :
        template = env.get_template("templates/about.html")
        self.response.write(template.render())

class ContributorsPage(webapp2.RequestHandler) :
    def get(self) :
        template = env.get_template("templates/contributors.html")
        self.response.write(template.render())

class EndGamePage(webapp2.RequestHandler) :
    def get(self) :
        sequence_key = self.request.get('sequence')
        # get the current_user with this sequence
        current_user = users.get_current_user()
        people = Person.query().fetch()
        current_email = current_user.email()
        current_person = Person.query().filter(Person.email == current_email).get()
        current_level = Level.query().filter(Level.player_key == current_person.key).filter(Level.sequence == str(sequence_key)).get()
        current_level.finished = True
        current_level.put()
        template = env.get_template("templates/end_game.html")
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/level", LevelPage),
    ("/create", CreateHandler),
    ("/about", AboutPage),
    ("/contributors", ContributorsPage),
    ("/end_game", EndGamePage),
], debug=True)
