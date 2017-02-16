from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template

from collection import Collection
from user import User
from card import Card
from item import Item

app = Flask(__name__)
app.secret_key = 'A2eZr98j/13y@4XR~XHH!w]emN]LWX/,?RT'

#App Clases
user = User()
coll = Collection()
crds = Card()
itm = Item()


@app.route("/")
def index():
    if session.get('login'): return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if not(session.get('login')): return redirect(url_for("login"))
    user.refresh()
    return render_template("collections/user_collections.html",user=session['user'])

# --------------------------------------------------------
#Definition of User Class routes
#------------------------------------------------------

@app.route("/users/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return user.signup(request)
    else:
        return render_template("users/signup.html")


@app.route("/users/login", methods=['GET', 'POST'])
def login():
    if session.get('login'):  return redirect(url_for("dashboard"))
    if request.method == 'POST':
        return user.login(request)
    else:
        return render_template("users/login.html")

@app.route("/users/logout")
def logout():
    session.pop('login', None)
    return redirect(url_for("login"))

@app.route("/users/update", methods=['GET', 'POST'])
def update_user():
    if not(session.get('login')):  return redirect(url_for("login"))
    if request.method == 'POST':
        return user.update(request)
    else:
        return render_template("users/update.html")

# --------------------------------------------------------
#Definition of Collection Class routes
#------------------------------------------------------
@app.route("/collection")
def collection():
    return "Available collections"

@app.route("/collections/add", methods=['GET', 'POST'])
def add_collection():
    if not(session.get('login')):  return redirect(url_for("login"))
    if request.method == 'POST':
        return coll.add(request)
    else:
        return render_template("collections/add.html")



@app.route("/collection/edit/<int:id>")
def edit_collection(id):
    return "Edit collection %d" % id


@app.route("/collection/delete/<int:collection>")
def delete_collection(collection):
    if not(session.get('login')):  return redirect(url_for("login"))
    return coll.delete(collection)

# --------------------------------------------------------
#Definition of Card Class routes
#------------------------------------------------------
@app.route("/cards")
def card():
    return "All Cards available"

@app.route("/collections/<int:collection>/cards/add", methods=['GET', 'POST'])
def add_card(collection):
    if not(session.get('login')):  return redirect(url_for("login"))
    if request.method == 'POST':
        return crds.add(request)
    else:
        return render_template("cards/add.html",coll=collection)

@app.route("/cards/edit/<int:id>")
def edit_card(id):
    return "You are editing a card %d" % id


@app.route("/cards/view/<int:id>")
def view_card(id):
    return "You are Viewing a card %d" % id


@app.route("/collection/<int:collection>/card/delete/<int:card>")
def delete_card(collection,card):
    if not(session.get('login')):  return redirect(url_for("login"))
    return crds.delete(collection,card)


@app.route("/collections/<int:collection>/cards/<int:card>/move", methods=['GET', 'POST'])
def move_card(collection, card):
    if not(session.get('login')):  return redirect(url_for("login"))
    if request.method == 'POST':
        return crds.move(request)
    else:
        return render_template("cards/move.html",coll=collection, cad = card)

# --------------------------------------------------------
#Definition of Card Class routes
#------------------------------------------------------

@app.route("/collections/<int:collection>/cards/<int:card>/items/add", methods=['GET', 'POST'])
def add_item(collection, card):
    if not(session.get('login')):  return redirect(url_for("login"))
    if request.method == 'POST':
        return itm.add(request)
    else:
        return render_template("items/add.html",coll=collection, cad = card)

@app.route("/collection/<int:collection>/card/<int:card>/items/delete/<int:item>")
def delete_item(collection,card,item):
    if not(session.get('login')):  return redirect(url_for("login"))
    return itm.delete(collection,card,item)

@app.route("/collection/<int:collection>/card/<int:card>/items/undo/<int:item>")
def undo_item(collection,card,item):
    if not(session.get('login')):  return redirect(url_for("login"))
    return itm.undo(collection,card,item)

if __name__ == "__main__":
    app.run(debug=True)
