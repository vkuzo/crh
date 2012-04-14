from django.conf import settings
from django.db import models
from geopy import geocoders, distance
from recycling.exceptions import gParseError, tooFarAwayError
from string import join
from unicodedata import normalize
import urllib

class RecycleType(models.Model):
	"""
	A type of recycling material (ex: aerosol cans, aluminum, light bulbs, etc.)
	"""
	
	name = models.CharField(max_length=100)
	desc = models.CharField(max_length=1000)
	#this is a char which containts comma separated sources
	#this probably needs to be moved into a separate table
	source = models.CharField(max_length=1000)
	
	desc.required = False
	
	def __unicode__(self):
		return self.name
		
	def getSources(self):
		"""
		Returns a list of the following:
		[
			[source domain, full source url],
			...
		]
		"""
		
		return [[x.strip(), x.replace('http:/','').split('/')[1]] for x in self.source.split(',')]
		
	def getSummary(self,address,index_low,index_high):
		"""
		Returns list of recyclers of this type close to (lat,lng)
		"""
		
		#geocode the address, return error if failed
		g = geocoders.Google()
		try:
			place, (lat, lng) = g.geocode(address)
		except (ValueError, geocoders.google.GQueryError):
			raise gParseError
			
		#if the distance is farther than n miles from Chicago, throw error
		dist_to_chicago = round(distance.distance((lat,lng), (settings.CHICAGO_LAT, settings.CHICAGO_LON)).miles,2)
		if dist_to_chicago >= settings.MAX_DISTANCE:
			e = tooFarAwayError()
			e.MAX_DISTANCE = settings.MAX_DISTANCE
			e.dist_to_chicago = dist_to_chicago
			raise e
			
		#if no errors so far, go ahead and compute and return the summary
		
		#get all recyclers
		recyclers = Recycler.objects.filter(recycleTypes=self)
		
		#get recycler summary
		results = [x.getSummary(lat=lat,lng=lng,startAddress=address) for x in recyclers]
		
		#sort by distance
		results = sorted(results, key = lambda x: x['distance'])
		
		#round distances (needs to be done after sorting) and add an index (similar to enumerate)
		for i in range(len(results)):
			results[i]['distance'] = round(results[i]['distance'],2)
			results[i]['index'] = i + 1
			results[i]['originCoords'] = (lat, lng)
		
		#cut off unneeded elements
		results = results[index_low-1:index_high]
		
		return results
		
class Recycler(models.Model):
	"""
	A site which accepts recycling materials
	"""
	
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	hours = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	website = models.URLField()
	lat = models.FloatField()
	lon = models.FloatField()
	comment = models.CharField(max_length=1000)
	source = models.CharField(max_length=1000)
	recycleTypes = models.ManyToManyField(RecycleType)
	isbluecart = models.NullBooleanField()	

	def __unicode__(self):
		return self.name
		
	def getDistance(self,lat,lng):
		"""
		Returns distance in miles from itself to (lat,lon)
		"""
		return distance.distance((lat, lng), (self.lat, self.lon)).miles		

	def getMaterialTypes(self):
		"""
		Returns a comma separated list of materials which this recycler accepts
		"""
		return join([str(x) for x in self.recycleTypes.all().order_by('name')], ", ")
	
	def getASCIIName(self):
		"""
		Returns string with name in ASCII
		"""
		return normalize('NFD', self.name).encode('ascii', 'ignore')	
	
	def getASCIIAdress(self):
		"""
		Returns string with address in ASCII
		"""
		return normalize('NFD', self.address).encode('ascii', 'ignore')	

	def getDrivingDirections(self, startAddress):
		"""
		Returns a url to Google driving directions from startAdress to this recycler
		"""
		params = {
			'saddr':startAddress,
			'daddr':self.getASCIIAdress()
		}
		encoded_params = urllib.urlencode(params)
		host = 'maps.google.com'
		path = '/maps'
		url = 'http://%s%s?%s' % (host, path, encoded_params)
		return url
		
	def getSummary(self,lat,lng,startAddress):
		"""
		Returns a summary of itself related to (lat,lng)
		"""
		return {
			'recycler':self,
			'distance':self.getDistance(lat,lng),
			'materials':self.getMaterialTypes(),
			'directions':self.getDrivingDirections(startAddress),
			}