import json
import pprint

from datetime import datetime
from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads

from flask import session, redirect, url_for

from model import Model


class User(Model):
    def __init__(self):
        super().__init__()

    def signup(self, request):
        firstname = request.form['fname']
        lastname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        # Check if this user email already exists
        data = self.todos.find({"user.email": email})
        for record in data:
            if record['user']['email'] == email: return redirect(url_for("signup"))

        data_id = self.todos.insert_one({
            "user": {"firstname": firstname, "lastname": lastname, "email": email, "password": password},
            "collection": []
        })

        return redirect(url_for("dashboard"))



    def update(self, request):
        current_password = request.form['current_password']
        password = request.form['password']
        email = session['user']['email']

        if current_password != session['user']['password']: return redirect(url_for("update_user"))
        
        result = self.todos.update_one({"user.email": email},{"$set": {"user.password": password}})

        if result.matched_count == 1:
            return redirect(url_for("dashboard"))
        return redirect(url_for("update_user"))

    def login(self, request):
        users = []
        email = request.form['email']
        password = request.form['password']

        data = self.todos.find({"user.email": email, "user.password": password}).limit(1)
        if data:
            for record in data:
                session['user'] = record['user']
                session['collection'] = record['collection']
                session['login'] = True
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("login"))

    def refresh(self):
        if session['login'] == False: return redirect(url_for("login"))
        email = session['user']['email']

        data = self.todos.find({"user.email": email}).limit(1)
        if data:
            for record in data:
                session['user'] = record['user']
                session['collection'] = record['collection']
                session['login'] = True
