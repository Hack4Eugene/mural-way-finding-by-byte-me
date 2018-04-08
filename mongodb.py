from pymongo import MongoClient
from bson import ObjectId
import pymongo
from DB import *

# # How Do I Drop a Collection?
# connection = pymongo.MongoClient("mongodb://admin:test@cluster0-shard-00-00-eouik.mongodb.net:27017,cluster0-shard-00-01-eouik.mongodb.net:27017,cluster0-shard-00-02-eouik.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
# connection.main.drop_collection("AdminSelfieQ.AdminSelfieQ")

# # Delete all Test Entries
# for entry in connection.main["Admin"].find({"admin_pw": "bidenB0i"}):
# 	connection.main["Admin"].remove(entry)

# def list_images(db):
# 	result = []
# 	for img in db["Mural"]:
# 		image_link = img["img_id"]
# 		img = db["Img"].find({"aws_link":})

def test_add_admin_selfie_queue():
	connection = pymongo.MongoClient("mongodb://admin:test@cluster0-shard-00-00-eouik.mongodb.net:27017,cluster0-shard-00-01-eouik.mongodb.net:27017,cluster0-shard-00-02-eouik.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
	dbMain = connection.main

	db = connection.main["AdminSelfieQ"]
	print("=================Printing All Entires in Mural=================\n")
	for img in db.find({}):
		print(img)

	print("=================Adding Entry to Admin Queue=================\n")
	add_selfie_to_queue(dbMain,"https://s3-us-west-2.amazonaws.com/muralwayfinderimages/murals/test.jpeg","5ac956c8e0d1bf01fe3b15fb")
	print("=================Printing All Entires in Mural=================\n")
	for img in db.find({}):
		print(img)

def test_process_selfie():
	connection = pymongo.MongoClient("mongodb://admin:test@cluster0-shard-00-00-eouik.mongodb.net:27017,cluster0-shard-00-01-eouik.mongodb.net:27017,cluster0-shard-00-02-eouik.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
	dbMain = connection.main

	db = connection.main["AdminSelfieQ"]
	print("=================Deleting Entry to Admin Queue=================\n")
	process_selfie(dbMain,True,"https://s3-us-west-2.amazonaws.com/muralwayfinderimages/murals/test.jpg")

	print("=================Printing All Entires in Mural=================\n")
	for img in db.find({}):
		print(img)

def display_all_db():
	connection = pymongo.MongoClient("mongodb://admin:test@cluster0-shard-00-00-eouik.mongodb.net:27017,cluster0-shard-00-01-eouik.mongodb.net:27017,cluster0-shard-00-02-eouik.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
	databases = connection.main.list_collection_names()
	db = connection.main
	for d in databases:
		print()
		print("Looking at Database: ",d)
		for entry in db[d].find({}):
			# if d == "AdminMuralQ":
			# 	print(entry["img_id"])
			print(entry)


# display_all_db()
# # test_add_admin_selfie_queue()
# # test_process_selfie()
# display_all_db()
connection = pymongo.MongoClient("mongodb://admin:test@cluster0-shard-00-00-eouik.mongodb.net:27017,cluster0-shard-00-01-eouik.mongodb.net:27017,cluster0-shard-00-02-eouik.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
databases = connection.main.list_collection_names()
db = connection.main
# process_mural(db,True,"https://s3-us-west-2.amazonaws.com/muralwayfinderimages/murals/b8671fd5-bfbf-40f9-a08c-3f6560ee5907.jpeg")
# # print(list(db["AdminMuralQ"].find({})))

# db["AdminMuralQ"].delete_one({"img_id":"https://s3-us-west-2.amazonaws.com/muralwayfinderimages/murals/b8671fd5-bfbf-40f9-a08c-3f6560ee5907.jpeg"})
display_all_db()
print(get_mural_queue(db))
print(get_selfie_queue(db))