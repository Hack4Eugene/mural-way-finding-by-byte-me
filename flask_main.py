import io
import logging
import sys
import uuid
import boto3
import flask
import DB
import aux_funcs
import pymongo
from PIL import Image
from botocore.client import Config
from flask import render_template
from flask import request
from flask import url_for
import CONFIG
from credentials import *


app = flask.Flask(__name__)

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
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
    return DB.add_image(db, bucket_str)


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
    lon = request.args.get('lon', 0, type=float)
    lat = request.args.get('lat', 0, type=float)
    images = DB.sorted_list(db, lon, lat)
    return images


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
    mongo_uri = "mongodb://{}:{}@{}"
    connection = pymongo.MongoClient(mongo_uri.format(DB_USER, DB_PASSWORD, DB_DOMAIN))

    try:
        db = connection.main
        print(db)

    except:
        print("Failure opening database.  Is Mongo running? Correct password?")
        sys.exit(1)
    if len(sys.argv) > 1:
        if sys.argv[1] == "adminsetup":
            #Hash admin password
			b_pw = ADMIN_PW.encode('UTF-8') #string needs to be in form: b'string'
			hashed = bcrypt.hashpw(b_pw, bcrypt.gensalt())
			if bcrypt.checkpw(b_pw, hashed): #TODO delete this if/else
				print('password hashed successfully')
			else:
				print('password hash error!!!')
			#Setup admin in database
            admin = db.Admin.find_one_and_update({"admin_id": ADMIN_ID},{'$set' :{ "admin_pw": hashed}})
            if admin is None:
                db.Admin.insert_one({'admin_id': ADMIN_ID, 'admin_pw' : hashed})

    #app.debug = CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT, host="0.0.0.0")