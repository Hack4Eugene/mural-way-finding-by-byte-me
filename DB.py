import pymongo
from aux_funcs import euclidean
from bson import ObjectId
from bson import objectid
from credentials import *
from botocore.client import Config



def sorted_list(db, lon=None, lat=None):
    records = []

    if lon is None or lat is None:
        for record in db.Mural.find({}).limit(30):
            records.append(record)
        records = sorted(records, key=lambda k: k['pageview'], reverse=True)
    else:
        for record in db.Mural.find({"type": "mural"}).limit(30):
            if record["lon"] and record["lat"]:
                dist = euclidean([lon,lat], [record["lon"],record["lat"]])
                records.append(record, dist)
        records = sorted(records, key=lambda k: k[1], reverse=True)
        records = [x[0] for x in records]
    return records


def add_mural_to_queue(db,lat,lon,name,address,artist,description,image):
    """
    @brief      Adds a new mural to the database

    @param      db           The database
    @param      lat          Photo latitude coordinate
    @param      lon          Photo longitude coordinate
    @param      name         The name of mural
    @param      address      The address (location) of mural
    @param      artist       The artist of the mural
    @param      description  The description
    @param      image        The image

    @return     None, updates the database with a new mural entry
    """

    entry = {
        "name": name,
        "lat": lat,
        "lon": lon,
        "artist": artist,
        "address": address,
        "description": description,
        "pageview": 0,
        "img_id": image,
        "selfies": []
        }

    #Then add mural to collection Mural
    result = db.AdminMuralQ.insert_one(entry)
  
    return True


def add_selfie_to_queue(db,img_id,mural_id):
    """
    @brief      Adds a selfie to AdminSelfie's queue.

    @param      db         The main database
    @param      img_id     The amazon web service image url
    @param      mural_id   The image identifier (links selfie to specific mural)

    @return     None, adds a selfie entry to db["AdminSelfieQ"]
    """

    entry = {
        "img_id": img_id,
        "mural_id": mural_id
    }
    db["AdminSelfieQ"].insert(entry)
    return None


def process_selfie(db, is_approved, aws_url):
    """
    @brief      processes a selfie in the admin's selfie queue

    @param      db           The database
    @param      is_approved(bool)  Indicates if the selfie has been approved
    @param      aws_url      The amazon web service image url

    @return     None, deletes the image from the queue and then attaches image to a mural's selfie list iff the image was approved.
    """

    selfie = db["AdminSelfieQ"].find_one({"img_id":aws_url})
    mural_id = selfie["mural_id"]
    if is_approved:
        mural = db["Mural"].find_one({"img_id":mural_id})
        # If the selfie image is not in the Mural's selfie list then add it
        if aws_url not in mural["selfies"]:
            selfies = mural["selfies"]
            selfies.append(aws_url)
            db["Mural"].update_one({"img_id":mural_id},{'$set':{"selfies":selfies}})

    else:
        pass
        # ADD AWS DELETION
        # I tried to add delete using Boto3 or boto but was not successful
    db["AdminSelfieQ"].delete_one({"img_id":aws_url})
    return None


def process_mural(db, is_approved, aws_url):
    """
    @brief      process a mural in the admin's mural queue

    @param      db            The database reference
    @param      is_approved   Indicates if the admin approves of the mural
    @param      aws_url       The amazon web service image url

    @return     None,         Delete the value from the queue and add the mural to the table
    """
    if is_approved:
        new = db["AdminMuralQ"].find_one({"img_id":aws_url})
        result = db["Mural"].insert_one(new)
        if result == None:
            print("Failed to add to mural queue")

    db["AdminMuralQ"].delete_one({"img_id":aws_url})
    return None

def get_mural_queue(db):
    return db["AdminMuralQ"].find_one({})

def get_selfie_queue(db):
    return db["AdminSelfieQ"].find_one({})