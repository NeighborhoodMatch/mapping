
import urllib2
import json
import import_files
import csv
import os
CENSUS_BENCHMARK = 'Public_AR_Current'
CENSUS_VINTAGE = 'Current_Current'
GEOCODING_URL = 'http://geocoding.geo.census.gov/geocoder/geographies/'
GEOCODE_DICTIONARY = os.path.join(os.path.dirname(__file__), '../..', 'data/geocode_library.json')
URL_COUNTER = [0] # To keep track of number of URLs added, used only when doing an online lookup
CHECKPOINT = 50

def create_geocode_dictionary(file_dictionary, run_geocode=False):
	'''
	Adds cenus tract data to overall dictionay keyed with address or lat/longs
	'''

	# Open existing library
	f = open(GEOCODE_DICTIONARY,'rb')
	geocode_dictionary = json.load(f)
	f.close()
	if run_geocode == False:
		return geocode_dictionary

	counter = 1
	in_dict_counter = 0

	# Loop through files and update all files
	for name in file_dictionary.keys():
		file_specs = file_dictionary[name]
		
		# Pass if file has tract already
		if 'census_tract' not in file_specs:
			filename = import_files.DATA_DIRECTORY + name
			
			# Checks what type of location data is in the file
			address = import_files.check_viable_columns(file_dictionary[name], 'address')
			lat_long = import_files.check_viable_columns(file_dictionary[name], 'lat/long')

	
			f = open(filename, 'rU')
			reader = csv.reader(f)			
			if file_specs['headers'] == 1:
				reader.next()

			# Loop through lines look up lat/longs first, then addresses
			for line in reader:
				found = 0					
				if lat_long != -1:
					
					# Checks if location has already been coded
					lat_long_string = lat_long_to_string(line, lat_long)
					
					if lat_long_string in geocode_dictionary:
						found = 1
						in_dict_counter += 1
						continue
					
					# Look up tract and add to geocode dictionary
					tract = call_for_census_tract(line, address, lat_long)
					if tract != -1:
						geocode_dictionary[lat_long_string] = tract
						found = 1

				# Repeat process for addresses if lat/long didn't return anything
				if (found == 0) and (address != -1):
					address_string = address_to_string(line, address)
					if address_string in geocode_dictionary:
						continue
					
					tract = call_for_census_tract(line, address, lat_long)
					
					if tract != -1:
						geocode_dictionary[address_string] = tract

				# Save dictionary in case internet/census site fails
				if counter % CHECKPOINT == 0:
					import_files.dump_to_file(geocode_dictionary, GEOCODE_DICTIONARY)
				
				# Helpful for monitoring geocoding process and IDing errors	
				print 'counter: ', counter, ',in dict: ', in_dict_counter, 'sum: ', counter + in_dict_counter
				counter += 1

				

	# Save file
	import_files.dump_to_file(geocode_dictionary,GEOCODE_DICTIONARY)

	return geocode_dictionary

# Helper functions

def look_up_census_tract(line, address, lat_long, geocode_dictionary):
	'''
	Looks up tract in geocode dictionary, checking for lat/long first
	'''
	if lat_long != -1:
		lat_long_string = lat_long_to_string(line, lat_long)
		if lat_long_string in geocode_dictionary:
			return geocode_dictionary[lat_long_string]
	
	if address != -1:
		address_string = address_to_string(line, address)
		if address_string in geocode_dictionary:
			return geocode_dictionary[address_string]
	else:
		return 'No Tract'

def lat_long_to_string(line, lat_long_locations):
	'''
	Takes the locations of a lat/long in a file and returns a consistent string
	'''
	return str(line[lat_long_locations[0][1]]) + ' ' + str(line[lat_long_locations[1][1]])

def address_to_string(line, address_locations):
	'''
	Takes the locations of address fields in a line and returns the string
	'''
	address_string = ''
	
	for item in address_locations:
		address_string = address_string + str(line[item[1]])

	return address_string

def call_for_census_tract(line, address_loc, lat_long_location):
	'''
	Gets census tract based on lat/long then address, returns first address match
	'''
	lookup = ''
	
	if lat_long_location != -1:
		
		# Build lat/long url string
		lookup_type = 'coordinates'
		lookup = 'coordinates?'
		for item in lat_long_location:
			if line[item[1]] == '':
				# Continue to address if no lat/longs
				lookup = ''
				break
			lookup = lookup + item[0] + '=' + str(urllib2.quote(line[item[1]])) + '&'
	
	if lookup == '':
		if address_loc == -1:
			return -1
		
		else:
			# Build string for address URLs
			lookup_type = 'address'
			lookup = 'address?'
			for item in address_loc:
				if line[item[1]] != '':
					lookup = lookup + item[0] + '=' + str(urllib2.quote(line[item[1]])) + '&'
			#returns if no data	
			if lookup == 'address?':
				return -1
		
	
	lookup = lookup + 'benchmark=' + CENSUS_BENCHMARK + '&vintage=' + CENSUS_VINTAGE + '&format=json'

	# Look up data on census site
	url = GEOCODING_URL + lookup


	print url, '# tested this session:', URL_COUNTER[0]
	URL_COUNTER[0] += 1

	# Error testing
	try:
		response = urllib2.urlopen(url)
	except Exception:
		print 'URL Error:' + url + " " + str(lat_long_location)
		return -1

	try:
		data = json.load(response)
	except Exception, e:
		print 'No json:' + url + ' ' + str(lat_long_location)
		return -1

	
	if lookup_type == 'address':
		try:
			tract = data['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['TRACT']
		except Exception, e:
			print 'dictionary error'
			return -1
	else:
		try:
			tract = data['result']['geographies']['Census Tracts'][0]['TRACT']
		except Exception, e:
			print 'dictionary error'
			return -1			

	print 'tract found:' ,tract
	return tract


if __name__ == '__main__':
	file_dictionary = import_files.create_file_dictionary()
	geocode_dictionary = create_geocode_dictionary(file_dictionary,True)
	








