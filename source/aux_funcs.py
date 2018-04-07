import pymongo
from pymongo import MongoClient

def euclidean(x, y):
    sumSq = 0.0

    # add up the squared differences
    for i in range(len(x)):
        sumSq += (x[i] - y[i]) ** 2

    # take the square root of the result
    return sumSq ** 0.5

def add_mural(db,name,address,description,image):
	"""
	@brief      Adds a mural to the database

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
	db.insert(entry)
	return None