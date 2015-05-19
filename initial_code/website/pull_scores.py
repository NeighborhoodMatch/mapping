import numpy as np
import sqlite3
DATABASE = 'tracts.db'


# Get data from database, standarize and convert to scores from 0-100
def call_data_base(query):
	'''
	Get data from SQL
	'''
	db = sqlite3.connect(DATABASE)
	c = db.cursor()
	data = c.execute(query).fetchall()
	return data

def get_average_score(input_data):
	'''
	Assumes tracts followed by all data and randomizes preferences
	'''

	numpy_data = np.array(input_data, dtype=np.float)
	# Convert no data to 0
	null_locations = np.isnan(numpy_data)
	numpy_data[null_locations] = 0
	
	tracts = numpy_data[:,0]
	data = numpy_data[:,1:]


	# Uncomment line to get constant results
	# constant_weights = [1 for x in np.arange(len(data[0]))]
	
	random_weights = [np.random.random() for x in np.arange(len(data[0]))]


	weighted_scores = np.average(data,axis=1,weights=random_weights)

	# Add tracts back in
	rv = np.c_[tracts,weighted_scores]
	
	return rv 
# Helper functions
def check_for_nearby_tracts(sorted_scores,N):
	'''
	Checks to make sure tracts aren't returned aren't next to each other
	'''
	rv = []
	tested = -1
	excluded = []
	while len(rv) < N and tested != N*-1:
		tract = int(sorted_scores[tested])
		tested -= 1
		if tract in excluded:
			continue
		rv.append(tract)
		select_statement = 'select census_2 from nearby_tracts where census_1 =' + str(tract)
		data = call_data_base(select_statement)
		new_data = [int(item[0]) for item in data]

		excluded = excluded + new_data
	return rv

def get_matching_tracts(args, sorted_scores):

	where = ''# Do somethng with args to convert to query

	select = 'select tract from multiple_tracts'
	query = select + where

	included_tracts = call_data_base(query)

	rv = []
	
	for tract in sorted_scores:
		if tract in included_tracts:
			rv.append(tract)
	
	return rv
# Main function for site to call

def go(N):
	'''
	Runs file and returns list of top N tracts
	'''

	scores = call_data_base('select * from score_table')
	scores = scores[1:] # Adjust for headers
	tract_scores = get_average_score(scores)
	sorted_scores = tract_scores[np.argsort(tract_scores[:,1])]
	#top_N_scores = check_for_nearby_tracts(sorted_scores[:,0],N)
	return sorted_scores[:N,0]

if __name__ == '__main__':
	pass

