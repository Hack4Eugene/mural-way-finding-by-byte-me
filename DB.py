import pymongo
from aux_funcs import euclidean
from bson import ObjectId


def sorted_list(db, lon, lat):
    records = []

    if lon is None or lat is None:
        for record in db.Mural.find({}).limit(30):
            records.append(record)
        records = sorted(records, key=lambda k: k['name'], reverse=True)
        records = [x["img_id"] for x in records]
    else:
        for record in db.Mural.find({"type": "mural"}).limit(30):
            dist = euclidean([lon,lat], [record["lon"],record["lat"]])
            records.append(record, dist)
        records = sorted(records, key=lambda k: k[1], reverse=True)
        records = [x[0]["img_id"] for x in records]

    return records


def add_image(db, aws_url):
    return


def add_mural(db,name,address,artist,description,image):
    """
    @brief      Adds a new mural to the database

    @param      db           The database
    @param      name         The name of mural
    @param      address      The address (location) of mural
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
        "pageload": 0,
        "img": image,
        "selfies": []
        }

    #First upload the image of the Mural to the file system
    filedata = grid.GridFS(db)
    upload_result = None #TODO

    #Then add mural to collection Mural
    collection = db.murals 
  

    return None