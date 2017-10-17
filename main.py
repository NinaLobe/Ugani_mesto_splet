#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
import random


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

#def class za drzavo
class Country():
    name = ""
    capital = ""

    def __init__(self,name, capital):
        self.name = name
        self.capital = capital

def GetData():
    slovenija = Country("Slovenije", "Ljubljana")
    croatia = Country("Hrvaske", "Zagreb")
    austrija = Country("Avstrije", "Dunaj")
    # drzave v array, da lahko nakljucno izberemo

    countries = [slovenija, croatia, austrija]
    return countries

class MainHandler(BaseHandler):
    def get(self):
        countries = GetData()
        country = countries[random.randint(0,len(countries)-1)]

        params = {"capital":country.name}

        return self.render_template("index.html",params=params)
    def post(self):

        guess = self.request.get("guess")
        country = self.request.get("country")
        countries = GetData()
        isCorrect = ""


        for i in countries:

            if i.name == country:
                if guess == i.capital:
                    isCorrect = "Cestitam, dobro poznas glavna mesta"
                elif guess == "":
                    isCorrect = "Vpisi drzavo"
                else:
                    isCorrect = "Poskusi se enkrat"

        country = countries[random.randint(0, len(countries) - 1)]
        params = {"correct":isCorrect, "capital":country.name}

        return self.render_template("index.html", params=params)





app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
