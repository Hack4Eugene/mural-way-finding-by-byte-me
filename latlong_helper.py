import exifread
#Adapted from/credit to: https://gist.github.com/snakeye/fdc372dbf11370fe29eb

def _to_degrees(value):
	"""
	Helper function to convert GPS coords to degrees (float)
	value is of type: exifread.utils.Ratio
	returns float
	"""
	d = float(value.values[0].num) / float(value.values[0].den)
	m = float(value.values[1].num) / float(value.values[1].den)
	s = float(value.values[2].num) / float(value.values[2].den)
	
	return d + (m / 60.0) + (s / 3600.0)
	
def lat_long(exif_data): #exif_data is a dictionary
	"""
	return lat/long from exif_data if it exists in full.
	Otherwise, return false.
	"""
	lat = None
	long = None
	
	try:
		gps_latitude = exif_data['GPS GPSLatitude']
		gps_longitude = exif_data['GPS GPSLongitude']
		gps_longitude_ref = exif_data['GPS GPSLongitudeRef']
		gps_latitude_ref = exif_data['GPS GPSLatitudeRef']
	except KeyError:
		return False
	
	lat = _to_degrees(gps_latitude)
	if gps_latitude_ref.values[0] != 'N': #We need to go negative, south
		lat = 0 -lat
		
	lon = _to_degrees(gps_longitude)
	if gps_latitude_ref.values[0] != 'E': #We need to go negative, west
		lon = 0 -lon
	
	return (lat,lon)
	
def read_file_lat_long(input_file):
	data = exifread.process_file(input_file)
	return lat_long(data)
	
