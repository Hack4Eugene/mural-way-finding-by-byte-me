import flask
import sys
import uuid
import aux_funcs
from flask import g
from flask import render_template
from flask import request
from flask import url_for
from PIL import Image, ImageFile
import json
import logging
import latlong_helper as llh # read_file_lat_long(input_file)
import boto3
from botocore.client import Config
import io

# Mongo database
from pymongo import MongoClient
import pymongo
# for use removing _ids
from bson.objectid import ObjectId

from credentials import *


mongo_uri = "mongodb://{}:{}@{}"
connection = pymongo.MongoClient(mongo_uri.format(DB_USER, DB_PASSWORD, DB_DOMAIN))

db = connection.test
print(db)
print(type(connection.main.Mural))
result = connection.main.Mural.insert_one({"test":"test"})
print(connection.main.Mural.find_one())

try:
    db = connection.test
    print(db)
    print(type(connection.main.Mural))
    #result = connection.main.Mural.insert_one({"test": "test"})
    #print(connection.main.Mural.find_one())
    mural_table = db.Mural.find({})

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

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

    # TODO:
    # Get lat/long(double)
    # Call method to add database using form information above
    # Number of Visits

    # TODO: call submit mural form
    # pass


@app.route("/_submit_photo", methods = ['GET', 'POST'])
def submit_photo():
    if request.method == 'POST':
        #title = request.form['title']
        #address = request.form['address']
        #description = request.form['description']
        im = request.files['file']
        im = Image.open(im)
        in_mem_file = io.BytesIO()
        im.save(in_mem_file, format="JPEG")
        s3 = boto3.resource(
            's3',
            aws_access_key_id = AWSAccessKeyId,
            aws_secret_access_key = AWSSecretKey,
            config=Config(signature_version='s3v4')
        )

        # Image Uploaded
        rng_str = 'murals/{}.jpeg'.format(str(uuid.uuid4()))
        bucket_str = 'https://s3-us-west-2.amazonaws.com/muralwayfinderimages/{}'.format(rng_str)
        s3.Bucket('muralwayfinderimages').put_object(Key=rng_str, Body=in_mem_file.getvalue(), ACL='public-read')

        return render_template("submit_mural.html", bucketsrc=bucket_str)


@app.route("/admin_login")
def admin_login():
    input_id = flask.request.form['username']
    input_pw = flask.request.form['password']
    b_pw = input_pw.encode('UTF-8')  ###string needs to be in form: b'string'
	
	admin = credentais[]
    
	if admin is None:
        print("Error: Meeting Not found")
        flask.g.iderror = True
        return render_template()
    if bcrypt.checkpw(b_pw, meeting['meeting_pw']):
        print('password checked successfully')
	else:
        print('password incorrect!!!')
        flask.g.passerror = True
        return render_template()
    #Probably want to set this as false at the beggining
	flask.session["admin_status"] = True
    return render_template()

@app.route("/logout")
def logout():
	flask.session["admin_status"] = False
	

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
        for record in mural_table.find({"type": "mural"}).sort("name", pymongo.ASCENDING):
            # TODO image logic
            records.append(record)

        records = sorted(records, key=lambda k: k['mural_name'], reverse=True)
    else:
        for record in mural_table.find({"type": "mural"}).sort("long_lat", pymongo.ASCENDING):
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
