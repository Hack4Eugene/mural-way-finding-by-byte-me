
import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

# Date handling
import arrow    # Replacement for datetime, based on moment.js
# import datetime # But we may still need time
from dateutil import tz  # For interpreting local times

# Mongo database
from pymongo import MongoClient
import pymongo
# for use removing _ids
from bson.objectid import ObjectId
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb+srv://{}:{}@{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.client_secrets.db)

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)
app.secret_key = CONFIG.secret_key

####
# Database connection per server process
###

try:
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)



###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  # TODO: Get Mural data from db to send to client
  return flask.render_template('index.html')


@app.route("/mural")
def mural():
    # TODO: Gets selfies using mural id and send to client
    pass


@app.route("/submit_mural")
def submit_mural():
    # TODO: call submit mural form
    pass


@app.route("/admin_login")
def admin_login():
    # TODO: DO LAST
    pass


@app.route("/create")
def create():
    app.logger.debug("Create")
    return flask.render_template('create.html')


@app.route("/_get_location")
def get_location():
    app.logger.debug("Get Location")
    pass

@app.route("/_set_order")
def set_order():
    # Pulls Mural data from mongo and sets order
    # TODO: This may not work
    long = request.args.get('long', 0, type=double)
    lat = request.args.get('lat', 0, type=double)

    if long is None or lat is None:
        # TODO: Fix to catch error
        # TODO: Get request from DB
        pass

    # TODO: Get request from DB
    pass

@app.route()


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

def euclid_dist():
    # TODO: Use to sort by distance
    pass

def upload_selfie():
    # TODO: Upload picture to separate

if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")
