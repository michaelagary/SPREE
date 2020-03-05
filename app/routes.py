import os
from app import app
from flask import render_template, request, redirect, session, url_for

from flask_pymongo import PyMongo

app.config['MONGO_DBNAME'] = 'SPREE'

app.config['MONGO_URI'] = 'mongodb+srv://dbUser:4wmJFdZIxF9JQ0Rg@cluster0-frdoa.mongodb.net/SPREE?retryWrites=true&w=majority'
import requests

mongo = PyMongo(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# INDEX

@app.route('/')
@app.route('/index')

def index():
    collection = mongo.db.SPREE
    SPREE = collection.find({})
    return render_template('index.html')


# CONNECT TO DB, ADD DATA

@app.route('/login', methods=['POST', 'GET'])
def login():
    collection = mongo.db.SPREE
    users = collection.users
    # login_user = collection.find_one({"email" : request.form["email"]})
    if request.method == 'POST':
        session['username'] = request.form['email']
        # session['password'] == request.form['password']
        return redirect(url_for('profile'))
            #profile page will display user's favroites and requests
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index')

@app.route('/profile')
def profile():
    collection = mongo.db.SPREE
    email = session['username']
    # information = collection.find({"favorites": "favorites", "requests": "requests"})
    return render_template('profile.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    users = mongo.db.users
    if request.method == 'POST':
        existing_user = users.find_one({'email' : request.form['email']})
        print("the request method is post", existing_user)
        if existing_user is None:
            users.insert({'email' : request.form['email'], 'password1': request.form['password1'], 'password2': request.form['password2']})
            if request.form['password1'] == request.form['password2']:
                session['username'] = request.form['email']
                return redirect('/store')
            else:
                return 'the two passwords must match!'
        return 'there is already a user with that email! try logging in'
    return render_template('signup.html')

@app.route('/store')
def store():
    collection = mongo.db.items
    # i did a query and thne turned it into a lsit of dictionaries
    items = list(collection.find({}))
    print("the items are ", items)
    # query mongo for all items
    # send list of items when rendering
    return render_template('store.html', items = items)

# GOAL: get all details about an item from Mongo and send it to build base page
@app.route('/item', methods=['POST', 'GET'])
def item():
    item_selected = dict(request.form)
    print("the information for the selected item is", item_selected)
    name = item_selected["name"]
    print(name)
    collection = mongo.db.items
    information = list(collection.find({"name": name}))
    print(information)
    # return 'page in progress'
    return render_template('item.html', items = information)
    # for the item selected by the user on the store page
# get ID from previous page (store.html)
# find in Mongo, store as item
# return render_template('item.html', item = (result of findginkt the item in Mongo))

@app.route('/admin', methods = ["GET", "POST"])
def admin():
    code = "0610"
    user_info = dict(request.form)
    if request.method == "GET":
        return render_template('admin.html')
    else:
        code2 = user_info["code"]
        if code2 == code:
            return render_template('new-item.html')
        else:
            # flash("the code you entered is inccorect")
            return redirect('/index')

@app.route('/new_item', methods = ["GET", "POST"])
def new_item():
    collection = mongo.db.items
    user_info = dict(request.form)
    name = user_info["name"]
    print("the item is " + name)
    description = user_info["description"]
    print("it is " + description)
    price = user_info["price"]
    print("it costs " + price)
    url = user_info["url"]
    print("the link to the item is: " + url)
    image = user_info["image"]
    print("the link to the item's image is: " + image)
    collection.insert({"name": name, "description": description, "price": price, "url": url, "image": image})
    message = "the item has been added to the store"
    return render_template('store.html', message = message)

@app.route('/sort50')
def sort50():
    collection = mongo.db.items
    items = collection.find({})
    fifty_and_under = []
    for item in items:
        print(item["price"])
        if float(item["price"]) <= 50 and float(item["price"]) >= 0:
            fifty_and_under.append(item)
            print("items $50 and under are, ", fifty_and_under)
    return render_template('store.html', items = fifty_and_under)

@app.route('/sort100')
def sort100():
    collection = mongo.db.items
    items = collection.find({})
    fifty_to_hundred = []
    for item in items:
        print(item["price"])
        if float(item["price"]) <= 100 and float(item["price"]) >= 50:
            fifty_to_hundred.append(item)
            print("items $50 to $100 are, ", fifty_to_hundred)
    return render_template('store.html', items = fifty_to_hundred)

# next step is go to store and add jinja templating {{ list }}
# so that when person decides to sort it displays items in that list
