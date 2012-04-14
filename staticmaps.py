#Google Maps API wrapper
#by Vasiliy Kuznetsov

class staticMap():
	
	# Google Maps Image API wrapper
	# API doc: http://code.google.com/apis/maps/documentation/imageapis/index.html
	# inputs:
	# width, height - size of image
	# center - (lat, lon) tuple of map center
	# markers - [(lat, lon), (lat2, lon2), ...] list of tuples of additional markers
	# output: url of needed map
	
	def __init__(self, width, height, center, markers):
		self.width = width
		self.height = height
		self.center = center
		self.markers = markers
		
	def getUrl(self):
		#returns ready url of needed map
		myurl = "http://maps.googleapis.com/maps/api/staticmap?"
		myurl += "center=%s,%s" % (self.center[0], self.center[1])
		myurl += "&size=%sx%s" % (self.height, self.width)
		#add center marker
		myurl += "&markers=color:red%7C" + "%s,%s" % (self.center[0], self.center[1])
		#add other markers, if they exist
		if len(self.markers)>0:
			for point in self.markers:
				myurl += "&markers=color:blue%7Clabel:" + "%s" % point[4]
				myurl += "%7C" + "%s,%s" % (point[0], point[1])
		else:
			myurl += "&zoom=10"
		myurl += "&sensor=false"
		return myurl