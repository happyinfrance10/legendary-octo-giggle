#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
    level_number = ndb.IntegerProperty()
    hint = ndb.StringProperty()
    second_hint = ndb.StringProperty()

class Level(ndb.Model): #keeps track of player progress per sequence
    player_key = ndb.KeyProperty()
    current_level = ndb.IntegerProperty()
    sequence = ndb.StringProperty()
    finished = ndb.BooleanProperty()

#when you create new questions, use the form
#tech questions (super hard lel)
question1_1 = Question(sequence="1", question="Lorem ipsum doloar sit amet, consecteturd adipiscin edlit, sed do eiusmd tempor incididunt ut labre et dolore mana aliqua. Ut enim ad minim venriam, quis nostrud exercietation ulamco laboris nisi sut aliquips ex a commodo consequat. (HQ)", answer = "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA", level_number=1, hint ="This looks largely like some lorem ipsum text, but are you sure it's copied verbatim down to the letter?", second_hint="After cross-referencing it with the corresponding text that seems to be the source, the difference in letters should spell out a company name and what to look for. Of course it may not be obvious which office but if that’s the case why is (HQ) there?")
question1_1.put()
question1_2 = Question(sequence="1", question="(1/2) People these days are going to #SiliconValley for jobs in the technological industry. Do they pay well? I came down to see for myself. <br> 8:48AM - 29 MAY 2015 <br><br>(2/2) I searched for a reputable tech company on some street. I think I found the building but don't know which door to knock on…<br> 8:48AM - 29 MAY 2015", answer = "900", level_number=2, hint ="If you live in an apartment and have had to fill out address line 2, this question may be easier for you. You might also want to count the number of characters per each paragraph. (Note the date listed!)", second_hint="(1/2) and (2/2) are associated with a social platform due to character limits imposed per status. Could this social platform be the company the narrator is looking for? (Again, note the date; the limit may have not been the same all the time…) In addition, the apartment number (which identifies the door to knock on) is analogous to the office suite number...")
question1_2.put()
question1_3 = Question(sequence="1", question="One fine day a couple years back (I don't know exactly how many years ago, I can't count), I used to work somewhere in the vicinity of the 145 and 161 highways. I moved out recently, but as I was leaving it seems like some other start-up is starting to take shape nearby. I don't bike, and can't use it. Thus, I don't recall the name. Do you?", answer = "LimeBike", level_number=3, hint ="Hint: The narrator can’t count in our base, but (s)he could count in another...", second_hint="After converting the highway numbers to a more readable form and searching for a bicycle startup in the area where they intersect, I would assume that there should be one name sticking out to your eyes...")
question1_3.put()

question2_1 = Question(sequence = "2", question = "Find the address of Germany's oldest zoo.", answer = "Hardenbergplatz 8, 10787 Berlin, Germany", level_number = 1, hint = "Google it!", second_hint = "Have you Googled it yet?")
question2_1.put()
question2_2 = Question(sequence = "2", question = "Find the address of the world's first zoo.", answer = "Maxingstraße 13b, 1130 Wien, Austria", level_number = 2, hint = "Google is your friend.", second_hint = "Located in Vienna, Austria (well, at least it's now called that)")
question2_2.put()
question2_3 = Question(sequence = "2", question = "Find the address of a zoo in the United States that opened in 1899.", answer = "2300 Southern Blvd, Bronx, NY 10460, USA", level_number = 3, hint = "The first zoo in the western hemisphere that had snow leopards.", second_hint = "Located in New York")
question2_3.put()
question2_4 = Question(sequence = "2", question = "Name the famous zoo not too far away from building blocks.", answer = "San Diego Zoo", level_number = 4, hint = "Located in CA", second_hint = "The building blocks are Legos...")
question2_4.put()
question2_5 = Question(sequence = "2", question = "Find the zoo that is famously known for its open design.", answer = "Singapore Zoo", level_number = 5, hint = "Located in Asia", second_hint = "Located in Singapore")
question2_5.put()

question3_1 = Question(sequence = "3", question = "When I was young, I visited South America, where I saw thousands and thousands of plants and birds. What was that place called?", answer = "Amazon Rainforest", level_number = 1, hint = "Try looking in Brazil.", second_hint = "There are lots of trees there!")
question3_1.put()
question3_2 = Question(sequence = "3", question = "I know of a place whose boundaries are noted by trees, but they’re not the trees you’re used to seeing. There isn’t too much water around here…", answer = "Mojave Desert", level_number = 2, hint = "Commonly called “The High Desert”", second_hint = "This North American desert crosses multiple states.")
question3_2.put()
question3_3 = Question(sequence = "3", question = "They say when you’re lost, follow the stream, but this one is too long to follow all the way. I hear this water has two colors. What’s it called?", answer = "Nile River", level_number = 3, hint = "Try looking in Africa", second_hint = "It's the primary water source of Egypt and Sudan.")
question3_3.put()
question3_4 = Question(sequence = "3", question = "Last March, I visited Scotland and saw a hexagon formed from lava flow. I was only able to visit because the water level was low. Where was I?", answer = "Fingal's Cave", level_number = 4, hint = "It is a cave.", second_hint = "Its upper and lower surfaces are cooled lava.")
question3_4.put()
question3_5 = Question(sequence = "3", question = "I’ve never felt as cold as I did as I visited this place in Asia. It was so tall, and I couldn’t breathe…", answer = "Mount Everest", level_number = 5, hint = "It is a mountain near Nepal and China.", second_hint = "It is miles tall.")
question3_5.put()

question4_1 = Question(sequence="4", question="Name the place where our founding fathers intended to revise the Articles of Confederation.", hint="This place is famous for the adoption of the Declaration of Independence in 1776", second_hint="It is presently called Independence Hall.", level_number=1, answer="Pennsylvania State House")
question4_1.put()


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

            # for tech sequence
            current_level_1 = Level.query().filter(Level.player_key == current_person.key).filter(Level.sequence == "1").get()
            # if the current user has no level progress, then create a new sequence
            if not current_level_1:
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

            # for animals/zoo sequence
            current_level_2 = Level.query().filter(Level.player_key == current_person.key).filter(Level.sequence == "2").get()
            # if the current user has no level progress, then create a new sequence
            if not current_level_2:
                current_level_2 = Level(player_key = current_person.key, current_level=1, sequence="2", finished=False)
                current_level_2.put()
            # if the current user finished the level, then reset progress
            if (current_level_2.finished):
                current_level_2.finished = False
                current_level_2.current_level = 1
                current_level_2.put()
            # loads correct question from within sequence 1
            current_question_2 = Question.query().filter(Question.sequence == current_level_2.sequence).filter(Question.level_number == current_level_2.current_level).get()
            if current_question_2:
                sequence2_key = current_question_2.key.urlsafe()
            else:
                sequence2_key = None
            #for wildlife/natural resources sequence
            current_level_3 = Level.query().filter(Level.player_key == current_person.key).filter(Level.sequence == "3").get()
            # if the current user has no level progress, then create a new sequence
            if not current_level_3:
                current_level_3 = Level(player_key = current_person.key, current_level=1, sequence="3", finished=False)
                current_level_3.put()
            # if the current user finished the level, then reset progress
            if (current_level_3.finished):
                current_level_3.finished = False
                current_level_3.current_level = 1
                current_level_3.put()
            # loads correct question from within sequence 1
            current_question_3 = Question.query().filter(Question.sequence == current_level_3.sequence).filter(Question.level_number == current_level_3.current_level).get()
            if current_question_3:
                sequence3_key = current_question_3.key.urlsafe()
            else:
                sequence3_key = None
            # for history (example) sequence
            current_level_4 = Level.query().filter(Level.player_key == current_person.key).filter(Level.sequence == "4").get()
            # if the current user has no level progress, then create a new sequence
            if not current_level_4:
                current_level_4 = Level(player_key = current_person.key, current_level=1, sequence="4", finished=False)
                current_level_4.put()
            # if the current user finished the level, then reset progress
            if (current_level_4.finished):
                current_level_4.finished = False
                current_level_4.current_level = 1
                current_level_4.put()
            # loads correct question from within sequence 1
            current_question_4 = Question.query().filter(Question.sequence == current_level_4.sequence).filter(Question.level_number == current_level_4.current_level).get()
            if current_question_4:
                sequence4_key = current_question_4.key.urlsafe()
            else:
                sequence4_key = None
        else:
            sequence1_key = None
            sequence2_key = None
            sequence3_key = None
            sequence4_key = None

        logout_url = users.create_logout_url("/")
        login_url = users.create_login_url("/")

        templateVars = {
            "people" : people,
            "current_user" : current_user,
            "login_url" : login_url,
            "logout_url" : logout_url,
            "current_person" : current_person,
            "sequence1_key" : sequence1_key,
            "sequence2_key" : sequence2_key,
            "sequence3_key" : sequence3_key,
            "sequence4_key" : sequence4_key,
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
