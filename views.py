from django.template import RequestContext
from django.shortcuts import render_to_response
from recycling.staticmaps import staticMap
from recycling.pagination import paginationList
from recycling.exceptions import gParseError, tooFarAwayError
from recycling.forms import *
from recycling.models import *

def main_page(request):
	if 'address' in request.GET:
		form = AddressForm(request.GET)
		if form.is_valid():
			
			address = form.cleaned_data['address']
			index_low = int(request.GET['index_low'])
			index_high = int(request.GET['index_high'])
			rectype = RecycleType.objects.get(name=form.cleaned_data['type'])

			#get summary for each recycling center which matches our type, handle errors
			try:
				results = rectype.getSummary(address, index_low, index_high)
			except gParseError:
				variables = RequestContext(request, {'form':form,
					'errormessage':"""The address you entered was not successfully parsed by Google Maps. 
						Please enter a valid Chicago address. To test the validity of your address, 
						try entering it into <a href="http://maps.google.com" target="_blank">Google Maps</a>."""
					})
				return render_to_response('main_page.html', variables)			
			except tooFarAwayError as e:
				variables = RequestContext(request, {'form':form, 
					'errormessage':'The address you entered is %s miles away from Chicago. Please enter an address within %s miles of Chicago.' % (e.dist_to_chicago, e.MAX_DISTANCE)
					})
				return render_to_response('main_page.html', variables)				
			
			#create point input for static maps						
			points = [(row['recycler'].lat, row['recycler'].lon, row['recycler'].getASCIIName(), "icon", row['index']) for row in results]

			#calculate maximum distance between center and point for javascript maps
			if len(results)>0: maxdistance = results[-1]['distance']
			else: maxdistance = 1
				
			#render
			variables = RequestContext(request, {'form':form,'results':results,
				'map_static':staticMap(350,450,results[0]['originCoords'],points).getUrl(),
				'maxDistance': maxdistance,
				'rectype':rectype,
				'rectype_sources':rectype.getSources(),
				'bottom_nav':paginationList(len(Recycler.objects.filter(recycleTypes=rectype))),
				'lat':results[0]['originCoords'][0],
				'lon':results[0]['originCoords'][1]})
			return render_to_response('main_page.html', variables)
	
	else:
		form = AddressForm()
	variables = RequestContext(request, {'form':form})
	return render_to_response('main_page.html',	variables)
	
def about_page(request):
	#get distinct list of sources
	dist = Recycler.objects.values('source').distinct()
	
	#build list of distinct sources
	sources = [x['source'] for x in dist if len(x['source'])>0]
	sources.sort()

	return render_to_response('about.html', {'sources':sources})