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
    return render_template('index.html', SPREE = SPREE)


# CONNECT TO DB, ADD DATA

@app.route('/add')
def add():
    # connect to the database
    collection = mongo.db.SPREE
    # insert new data
    collection.items.insert({"item": "pants", "price": "17.99"})
    # return a message to the user
    return "item added"

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

@app.route('/cardigan')
def cardigan():
    return render_template('cardigan.html')

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/sweater')
def sweater():
    return render_template('sweater.html')

@app.route('/lace-detail')
def lacedetail():
    return render_template('lace-detail.html')

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

# THIS IS HOW FILTER WORKS https://www.geeksforgeeks.org/filter-in-python/
# filter(function, sequence)
# Parameters:
# function: function that tests if each element of a
# sequence true or not.
# sequence: sequence which needs to be filtered, it can
# be sets, lists, tuples, or containers of any iterators.
# Returns:
# returns an iterator that is already filtered.

# THIS IS HOW TO CREATE A FILTER TO SORT THROUGH ITEMS BASED ON price
# function that filters vowels
# def fun(variable):
#     letters = ['a', 'e', 'i', 'o', 'u']
#     if (variable in letters):
#         return True
#     else:
#         return False
#
# My practice version
# def sort1(variable):
# range = range(0,51.99)

# def sort2(variable):
# range = range(51.99,100.99)
# # sequence
# sequence = ['g', 'e', 'e', 'j', 'k', 's', 'p', 'r']
#
# # using filter function
# filtered = filter(fun, sequence)
#
# print('The filtered letters are:')
# for s in filtered:
#     print(s)
