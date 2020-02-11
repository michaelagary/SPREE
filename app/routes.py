import os
from app import app
from flask import render_template, request, redirect


# from flask_pymongo import PyMongo

# name of database
# app.config['MONGO_DBNAME'] = 'database-name'

# URI of database
# app.config['MONGO_URI'] = 'mongo-uri'

# mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/cardigan')
def cardigan():
    return render_template('cardigan.html')

@app.route('/sweater')
def sweater():
    return render_template('sweater.html')

@app.route('/lace-detail')
def lacedetail():
    return render_template('lace-detail.html')
