import sys
import simplejson
import httplib2
import time
import csv
import datetime
import traceback

FS_API_URL = "https://api.foursquare.com/v2/"
LOCATIONS = []

def get_access_token(token_file):
	return open(token_file, 'r').read()

def get_venues(ll, query, fs_token):
		h = httplib2.Http()
		url = get_venues_search_url(ll, query, fs_token)
		resp, content = h.request(url)
		json = simplejson.loads(content)
		return json["response"]["venues"]

def get_venues_search_url(ll, query, fs_token):
	t = time.strftime("%Y%m%d")
	return FS_API_URL + "venues/search?ll=" + ll + "&limit=50&query=" + query + "&oauth_token=" + fs_token + "&v=" + t
		
def get_venues_union(venues_lst):
	results = {}
	
	for venues in venues_lst:
		for venue in venues:
			venue_id = venue["id"]
			venue_name = venue["name"]
			venue_city = "";
			venue_checkins = venue["hereNow"]["count"]
			
			try:
				venue_city = venue["location"]["city"]
			except:
				venue_city = "undefined"
				
			results[venue_id] = {"id": venue_id, "venue_name": venue_name, "venue_city": venue_city, "venue_checkins": venue_checkins}
		
	return results
	
def gather_stats(query, locations, out_file, fs_token):
		#Round datetime to nearest 15 minutes
		t_now = datetime.datetime.now()
		t_rounded = t_now - datetime.timedelta(minutes = t_now.minute % 15, seconds = t_now.second, microseconds = t_now.microsecond)
				
		t = time.strftime("%Y-%m-%d %H:%M:%S")
		
		results =  csv.writer(open(out_file, 'ab+'), delimiter=';', quotechar='|', dialect='excel')
		responses = map(lambda ll:get_venues(ll, query, fs_token), locations)		
		venues = get_venues_union(responses)
		
		c = 0
		
		for venue in venues:
			c += int(venues[venue]["venue_checkins"])
			results.writerow([t_rounded, venues[venue]["id"], venues[venue]["venue_name"], venues[venue]["venue_city"], venues[venue]["venue_checkins"]])
		
		print "Ticked @ " + str(t_rounded) + ", total checkins: " + str(c)
		
def run_gather_stats(query, delay, locations, out_file, fs_token):
	while (1 > 0):
		try:
			gather_stats(query, locations, out_file, fs_token)
		except Exception:
			print "Oops, something went wrong..."
			traceback.print_stack()
			print sys.exc_info()[1]
		time.sleep(delay)
		
def run(args):
	cur_arg = "command"
	
	try:
		cur_arg = "query"
		query = args[0]
		cur_arg = "delay"
		delay = int(args[1]) * 60
		cur_arg = "token file"
		fs_token_file = args[2]
		cur_arg = "locations file"
		locations_file = args[3]
		cur_arg = "out file"
		out_file = args[4]
		cur_arg = "args ok"
		
		fs_token = get_access_token(fs_token_file)
		print "Token = " + fs_token
		locations = open(locations_file, "r").read().split("\n")
		print "Locations: " + str(len(locations))
	
		run_gather_stats(query, delay, locations, out_file, fs_token)
	
	except Exception:
		print "Something went wrong while parsing arguments."
		print "Missing argument: " + cur_arg
		print sys.exc_info()[1]

run(sys.argv[1:len(sys.argv)])
