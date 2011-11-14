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


def get_venues(ll, query):
		h = httplib2.Http()
		url = FS_API_URL + "venues/explore?ll=" + ll + "&limit=50&query=" + query + "&oauth_token=" + FS_ACCESS_TOKEN + "&v=20110828"
		resp, content = h.request(url)
		json = simplejson.loads(content)
		return json["response"]["venues"]
		

def run():
		results = open("queryresults.csv", "w+")

		for venue in get_venues("51.048301,3.74221", "colruyt"):
			city = ""
			
			try:
				city = venue["location"]["city"]
			except:
				city = "unknown"
			
			results.write(venue["name"] + "," + city  + "," + venue["id"] +"\n")

		results.flush()
		results.close()
	
run()