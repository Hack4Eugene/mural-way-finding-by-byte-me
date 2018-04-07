import pymongo
from pymongo import MongoClient

def euclidean(x, y):
    sumSq = 0.0

    # add up the squared differences
    for i in range(len(x)):
        sumSq += (x[i] - y[i]) ** 2

    # take the square root of the result
    return sumSq ** 0.5

def add_mural(db,image,title,address,description):
	"""
	@brief      Adds mural to database.
	
	@param      db           The database
	@param      image        The image
	@param      title        The title of mural
	@param      address      The address of mural
	@param      description  The description for mural
	
	@return     None, updates the database with a new mural entry
	"""
	return None