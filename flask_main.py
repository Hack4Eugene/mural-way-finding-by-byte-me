import flask
import sys
import aux_funcs
from flask import g
from flask import render_template
from flask import request
from flask import url_for
from PIL import Image
import json
import logging

# Mongo database
from pymongo import MongoClient
import pymongo
# for use removing _ids
from bson.objectid import ObjectId

'''
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb+srv://{}:{}@{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.client_secrets.db)
'''

###
# Globals
###
import CONFIG

app = flask.Flask(__name__)
#app.secret_key = CONFIG.secret_key

####
# Database connection per server process
###
'''
try:
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)
'''

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    # TODO: Get Mural data from db to send to client
    return render_template('index.html')


@app.route("/mural")
def mural():
    # TODO: Gets selfies using mural id and send to client
    pass


@app.route("/submit_mural")
def submit_mural():
    app.logger.debug("Submit Mural page entry")
    return render_template("submit_mural.html")
    #title = request.form['title']
    #address = request.form['address']
    #description = request.form['description']
    # TODO:
    # Get lat/long(double)
    # Call method to add database using form information above
    # Number of Visits

    # TODO: call submit mural form
    # pass


@app.route("/_submit_photo", methods = ['GET', 'POST'])
def submit_photo():
    if request.method == 'POST':
        image = request.files['file']
        im = Image.open(image)
        print(image)
        return render_template("submit_mural.html", message=im)


@app.route("/admin_login")
def admin_login():
    # TODO: DO LAST
    pass


@app.route("/create")
def create():
    app.logger.debug("Create")
    return render_template('create.html')


@app.route("/_get_location")
def get_location():
    app.logger.debug("Get Location")
    pass


@app.route("/_get_images")
def get_images():
    # Pulls Mural data from mongo and sets order
    # TODO: This may not work
    long = request.args.get('long', 0, type=float)
    lat = request.args.get('lat', 0, type=float)

    long_lat = [long, lat]

    records = []

    # TODO limit calling the entire DB
    if long is None or lat is None:
        # TODO: Fix to catch error
        for record in collection.find({"type": "mural"}).sort("name", pymongo.ASCENDING):
            # TODO image logic
            records.append(record)

        records = sorted(records, key=lambda k: k['mural_name'], reverse=True)
    else:
        for record in collection.find({"type": "mural"}).sort("long_lat", pymongo.ASCENDING):
            # TODO image logic
            records.append(record)
        # TODO edit to sort by euclidean distance
        records = sorted(records, key=lambda k: k['long_lat'], reverse=True)

    return records


@app.route("/_upload_selfie")
def upload_selfie():
    # TODO: Upload picture to separate
    # http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
    mural_name = request.args.get('mural_name', 0, type=str)

    test = {"type": "selfie", "mural": mural_name}
    collection.insert(test)
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404


if __name__ == "__main__":
    #app.debug = CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT, host="0.0.0.0")
