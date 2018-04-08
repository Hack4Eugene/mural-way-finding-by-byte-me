import pymongo


def sorted_list(db, lon, lat):
    records = []

    # TODO limit calling the entire DB
    if lon is None or lat is None:
        for record in mural_table.find({}).sort("name", pymongo.ASCENDING):
            records.append(record)

        records = sorted(records, key=lambda k: k['mural_name'], reverse=True)
    else:
        for record in mural_table.find({"type": "mural"}).sort("long_lat", pymongo.ASCENDING):
            # TODO image logic
            records.append(record)
        # TODO edit to sort by euclidean distance
        records = sorted(records, key=lambda k: k['long_lat'], reverse=True)

def add_image(db, aws_url):


def add_mural(db,name,address,description,image):
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