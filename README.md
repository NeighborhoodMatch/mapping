# mapping

Contains code that can be used to filter locations given a list of census tracts.
This code is covered by the license listed in the LICENSE file in this repository.

###############
Run Django website from initial_code>website $ python manage.py runserver
Navigate to http://127.0.0.1:8000/nmatch/home/

###############
Geocoding:
geocoding.py contains code to look up a census tract based on either a lat/long or address. It calls the census website (hardcoded) and is relatively slow. If you find a better way to get a census tract via API please replace!
geocode_library.json is a dictionary keyed with either addresses or lat/longs. This can be checked before doing a lookup. Geocoding.py also writes to here to prevent multiple lookups to the slow census site.

###############
Website:

nmatch/views.py:
Django survey open to editing

pull_scores.py:
Called from views. Currently pulls all rows and averages all scores randomly. Can be changed to return even weights to get consistent resuls. Also checks to make sure none of tracts being returned are in the same radius as any others (this may need to be removed if all tracts are returned). The current iteration returns a list of N tracts ranked from best to worst.

tracts.db: Full database with standardized scores. Includes
- nearby_tracts: Pairs of all tracts with centroids within a 1.25 km radius of each other. All combinations are includes (A,B) and (B,A). Also includes lat and long for census_1 of each row corresponding to the centroid
- raw_tract_data: Data by individual census tracts, columns should be relatively well named, all prefaces are general categories
- multiple_tracts: Same data as raw_tract_data but consolidated over all nearby tracts as determined by nearby_tracts database
- score_table: Weighted scores from 0-100 with 100 being the best besides for crime. Built off of multiple tracts database
