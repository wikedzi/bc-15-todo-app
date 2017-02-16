import json
import pprint

from datetime import datetime
from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads

from flask import session, redirect, url_for

from model import Model


class Item(Model):
    def __init__(self):
        super().__init__()

    def index(self):
        pass

    def add(self, request):
        coll = request.form['collection']
        card = request.form['card']
        item = request.form['item']
        email = session['user']['email']

        # Check if this user email already exists
        data = self.todos.find({"user.email": email}).limit(1)

        #for record in data:
            #for c in record['collection'][int(coll)]['cards']:
            	#for it in c[int(card)]["items"]:
                	#if it['label'] == item: return redirect(url_for("add_item"))


        result = self.todos.update({"user.email": email},
                               {"$push": {
                                   "collection." + coll + ".cards." + card +".items": {"$each": [{"label": item, "done": False}]}}})
        if result:
            return redirect(url_for("dashboard"))
        return redirect(url_for("add_item"))

    def undo(self, coll,cad,itm):
        email = session['user']['email']
        item_status = session['collection'][int(coll)]['cards'][int(cad)]['items'][int(itm)]['done']

        if item_status == True:
            item_status = False
        else:
            item_status = True

        result = self.todos.update_one({"user.email": email},{"$set": {"collection."+str(coll)+".cards."+str(cad)+".items."+str(itm)+".done":item_status}})
        return redirect(url_for("dashboard"))

    def delete(self, coll,cad,itm):
        email = session['user']['email']
        item_name = session['collection'][int(coll)]['cards'][int(cad)]['items'][int(itm)]['label']
        cleared = self.todos.update({"user.email": email},
                                        {"$pull": {"collection."+str(coll)+".cards."+str(cad)+".items":{"label":item_name}}})

        return redirect(url_for("dashboard"))