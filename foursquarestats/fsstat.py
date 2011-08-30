import simplejson
import httplib2
import time

OAUTH_BASE = "https://foursquare.com/oauth2/authenticate"
CLIENT_ID = "5J1DRUQHKVWUEUJO5I1UKLTPO2XV15RIOXEZZVQIP4FD0WUC"
CLIENT_SECRET = "O41ZMZSZCCG25JYJ4ABCX5IEQUPUKH4ES2R2XLIK1UF4GQGT"
CLIENT_CALLBACK = "http://www.dominiek.eu/ok"

FS_ACCESS_CODE = "EPIFSTLH2OPOHH45LVVLORSH5UD120MFV0VTWXXBLND23CO3"
FS_ACCESS_TOKEN = "KJWFAL4U22421FMRRE4OQ4K0NHVBYCUGS2TTGMW4F1KZNSRE"

FS_API_URL = "https://api.foursquare.com/v2/"

DELAY = 60 * 15

venues_to_check = ["185675"]

def get_checkins(venue_id):
		h = httplib2.Http()
		resp, content = h.request(FS_API_URL + "venues/" + venue_id + "/herenow?oauth_token=" + FS_ACCESS_TOKEN)
		json = simplejson.loads(content)
		return json["response"]["hereNow"]["count"]
		

def run():
	while (True):
		results = open("results.csv", "a+")
		t = time.strftime("%Y-%m-%d %H:%M:%S")
		records = map(lambda venue: [venue, get_checkins(venue)],venues_to_check)
		for record in records:
			results.write(t + "," + record[0] + "," + str(record[1]) + "\n")
		print "Fetched data @: " + t
		results.flush()
		results.close()
		time.sleep(DELAY)
	
run()