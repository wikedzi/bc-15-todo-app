import json
import pprint

from datetime import datetime
from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads

from flask import session, redirect, url_for

from model import Model


class Card(Model):
    def __init__(self):
        super().__init__()

    def index(self):
        pass

    def add(self, request):
        coll = request.form['collection']
        card = request.form['card']
        description = request.form['description']
        email = session['user']['email']

        # Check if this user email already exists
        data = self.todos.find({"user.email": email}).limit(1)

        for record in data:
            for c in record['collection'][int(coll)]['cards']:
                if c['label'] == card: return redirect(url_for("add_card"))

        result = self.todos.update({"user.email": email},
                                   {"$push": {
                                       "collection." + coll + ".cards": {"$each": [{"label": card, "description":description, "items": []}]}}})
        if result:
            return redirect(url_for("dashboard"))
        return redirect(url_for("add_card"))

    def move(self, request):
        coll = request.form['collection']
        new_coll = request.form['new_collection']
        card = request.form['card']
        email = session['user']['email']

        newCard = session['collection'][int(coll)]['cards'][int(card)]
        cardName = newCard['label']

        if coll == new_coll:
            return redirect(url_for("dashboard"))

        # Check if this user email already exists
        result = self.todos.update({"user.email": email},
                                   {"$push": {
                                       "collection." + new_coll + ".cards": {"$each": [newCard]}}})
        if result:
            cleared = self.todos.update({"user.email": email},
                                        {"$pull": {"collection." + coll + ".cards":{"label":cardName}}})
            return redirect(url_for("dashboard"))
        return redirect(url_for("add_card"))


    def delete(self, coll,cad):
        email = session['user']['email']
        card_name = session['collection'][int(coll)]['cards'][int(cad)]['label']
        cleared = self.todos.update({"user.email": email},
                                        {"$pull": {"collection."+str(coll)+".cards":{"label":card_name}}})

        return redirect(url_for("dashboard"))