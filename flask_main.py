import io
import logging
import sys
import uuid
import boto3
import flask
import DB
import aux_funcs
import pymongo
import bcrypt
from PIL import Image
from botocore.client import Config
from flask import render_template
from flask import request
from flask import url_for
import CONFIG
from credentials import *
from latlong_helper import *



app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())


###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    if 'admin_status' not in flask.session:
        flask.session['admin_status'] = False
        
    app.logger.debug("Main page entry")
    data = DB.sorted_list(db)
    app.logger.debug(len(data))
    app.logger.debug(data[0])
    return render_template('index.html', mural_data=data)


@app.route("/mural")
def mural():
    app.logger.debug("Mural page entry")
    image_url = flask.session["image_id"]
    mural_instance = db.Mural.find_one({"img_id":image_url})
    db.Mural.update({"img_id":image_url},{"$inc":{"pageview":1}})
    return render_template('mural.html', mural_instance = mural_instance)

@app.route("/submit_mural")
def submit_mural():
    app.logger.debug("Submit Mural page entry")
    return render_template("submit_mural.html")

@app.route("/_submit_photo", methods = ['GET', 'POST'])
def submit_photo():
    app.logger.debug("Submit Mural page entry")
    if request.method == 'POST':
        title = flask.session['title']
        address = flask.session['loc']
        description = flask.session['desc']

        im = request.files['file']
        i = 0
        for i in range(1000):
            i = i
        lat_lon = read_file_lat_long(im)
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

        if lat_lon:
            result = DB.add_mural_to_queue(db,lat_lon[0], lat_lon[1],title,address,"Unknown",description, bucket_str)
        else:
            result = DB.add_mural_to_queue(db,None, None,title,address,"Unknown",description, bucket_str)
        if not result:
            print("AGHHHH!")
    return render_template("submit_mural.html")

@app.route("/_test")
def test():
    app.logger.debug("Got a JSON request");
    title = request.args.get("title", 0, type=str)
    desc = request.args.get("desc", 0, type=str)
    loc = request.args.get("loc", 0, type=str)

    flask.session["title"] = title
    flask.session["desc"] = desc
    flask.session["loc"] = loc

    #TODO add to DB

    rslt = {"function": "/index"}
    return flask.jsonify(result=rslt)

@app.route("/admin",methods=["POST","GET"])
def admin():

    return render_template("admin.html")

@app.route("/admin_login", methods = ['POST', 'GET'])
def admin_login():
    """
    When the login button is clicked, check if the input credentials are legit.
    Set session keys based on what happens.HTML will respond accordingly.
    This function sets these:
        session: admin_status
              g: iderror, passerror, login_screen        
    """
    input_id = flask.request.form['username']
    input_pw = flask.request.form['password']
    print(input_id)
    print(input_pw)
    b_pw = input_pw.encode('utf-8') #sets ('string') to form: (b'string')
    admin = db.Admin.find_one({'admin_id': input_id})
    if admin is None:
        print("Error: Admin Not found")
        flask.g.iderror = True
        return render_template("admin.html")
    if bcrypt.checkpw(b_pw, admin['admin_pw']):
        print('password checked successfully')
        flask.session["admin_status"] = True
        flask.session["manage"] = False
        flask.session["next_mural"] = DB.get_mural_queue(db) and DB.get_mural_queue(db)["img_id"]
        flask.session["next_selfie"] = DB.get_selfie_queue(db) and DB.get_selfie_queue(db)['img_id']

        flask.g.login_screen = False
        return flask.redirect(flask.url_for("admin"))
    else:
        print('password incorrect!')
        flask.g.passerror = True
        return render_template("admin.html")

@app.route("/logout", methods = ["POST"])
def logout():
    """
    Logout and redirect back to index.
    """
    flask.session["admin_status"] = False
    
    return flask.redirect(flask.url_for("index"))

@app.route("/manage", methods = ["POST"])
def manage():
    """
    
    """
    flask.session["manage"] = True
    return flask.render_template("index.html")
    
@app.route("/review", methods = ['POST'])
def review():
    """
    Decide what to do based on what review button was pressed, using DB functions.
    Incoming: python black magic.
    """
    if "mural_t" in request.form:
        DB.process_mural(db, True, flask.session["next_mural"])
        flask.session["next_mural"] = DB.get_mural_queue(db) and DB.get_mural_queue(db)["img_id"]
    if "mural_f" in request.form:
        DB.process_mural(db, False, flask.session["next_mural"])
        flask.session["next_mural"] = DB.get_mural_queue(db) and DB.get_mural_queue(db)["img_id"]
    if "selfie_t" in request.form:
        DB.process_selfie(db, True, flask.session["next_selfie"])
        flask.session["next_selfie"] = DB.get_selfie_queue(db) and DB.get_selfie_queue(db)['img_id']
    if "selfie_f" in request.form:
        DB.process_selfie(db, False, flask.session["next_selfie"])
        flask.session["next_selfie"] = DB.get_selfie_queue(db) and DB.get_selfie_queue(db)['img_id']
    return render_template("/admin.html")

@app.route("/_ja")
def ja():
    """
    Helper function for ummmmmmmm what is it, main? or its. . . the one that starts wth an m.. Mural! - Wyatt
    """
    image_id = request.args.get("image_id", 0, type=str)
    print(image_id)
    flask.session["image_id"] = image_id
    rslt = {"function": "/mural"}
    return flask.jsonify(result=rslt)


@app.route("/delete",methods=["POST"])
def delete():
    # update_db.delete_from_db(db,request)
    print("=======================================")
    checked_murals = []
    form = request.form
    print(db["Mural"].count())
    # print(request.form.get("check1"))
    for i in range(1,db["Mural"].count()+1):
        try:
            aws_url = form["check{}".format(i)]
            checked_murals.append(aws_url)
        except:
            pass

    print(checked_murals)
    for mural in checked_murals:
        db["Mural"].remove({"img_id":mural})
    print("=======================================")
    return flask.redirect(url_for("index"))
    return None

@app.route("/_get_images")
def get_images():
    # Pulls Mural data from mongo and sets order
    lon = request.args.get('lon', 0, type=float)
    lat = request.args.get('lat', 0, type=float)
    images = DB.sorted_list(db, lon, lat)
    return images


@app.route("/_upload_selfie", methods=['POST'])
def upload_selfie():
    app.logger.debug("Submit Mural page entry")
    if request.method == 'POST':

        im = request.files['file']
        im = Image.open(im)
        in_mem_file = io.BytesIO()
        im.save(in_mem_file, format="JPEG")
        s3 = boto3.resource(
            's3',
            aws_access_key_id=AWSAccessKeyId,
            aws_secret_access_key=AWSSecretKey,
            config=Config(signature_version='s3v4')
        )

        # Image Uploaded
        rng_str = 'murals/{}.jpeg'.format(str(uuid.uuid4()))
        bucket_str = 'https://s3-us-west-2.amazonaws.com/muralwayfinderimages/{}'.format(rng_str)
        s3.Bucket('muralwayfinderimages').put_object(Key=rng_str, Body=in_mem_file.getvalue(), ACL='public-read')
        result = DB.add_selfie_to_queue(db, bucket_str, flask.session["image_id"])
        if not result:
            print("AGHHHH!")

    image_url = flask.session["image_id"]
    mural_instance = db.Mural.find_one({"img_id": image_url})
    return render_template("mural.html", mural_instance=mural_instance)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return render_template('page_not_found.html',
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
    #This can be extended to handle more commands. This is an easy way to allow setting up admins. There should not be too many, considering the use case.
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
    app.run(port=8000, host="0.0.0.0")