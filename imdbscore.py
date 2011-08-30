import urllib2
import urllib
import json
from operator import itemgetter
import sys
import re
import os
import csv
import logging

print "test"
readDirectory = sys.argv[1]
outputFile = sys.argv[2]

def getInfo(movieName):
	try:
		page = urllib2.urlopen("http://www.imdbapi.com/?t=" + movieName)
		data = "[" + page.readlines()[0] + "]"
		obj = json.loads(data)
		if (len(obj) > 0):
                        logging.debug("Retrieved response for: " + movieName)
                        return obj[0]
	except:
                logging.debug("Error getting response for: " + movieName)
		return None

def clean(name):
	return urllib.quote(re.sub(r'\([^)]*\)', '', name.strip().replace("."," ")))

def getMovieNames(folder):
	lst = os.listdir(folder)
	return map(lambda x:urllib.quote(x), lst)

def process(folder):
        movieNames = getMovieNames(folder)
        infos = [info for info in map(lambda movieName: getInfo(movieName), movieNames) if info != None]
        lst = []
        i = 0
        
        for info in infos:
                unquotedMovieName = urllib.unquote(movieNames[i])
                                           
                try:
                        lst.append([unquotedMovieName, info["Title"], float(info["Rating"]), info["Genre"], info["Runtime"]])
                except:
                        logging.warn("Error parsing response for: " + unquotedMovieName)
                i += 1
        return lst

results = process(readDirectory)
writer = csv.writer(open(outputFile, 'wb'), delimiter=';', quotechar='|',quoting=csv.QUOTE_MINIMAL)                                
map(lambda row:writer.writerow(row), results)
