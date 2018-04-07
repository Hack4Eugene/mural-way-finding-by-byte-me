import latlong_helper as llh

if __name__ == "__main__":
	f = open("test.jpg", 'rb')
	print(llh.read_file_lat_long(f))