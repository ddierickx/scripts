import urllib2
import urllib
import json
from operator import itemgetter
import sys
import re
import os

def getScore(movieName):
	try:
		page = urllib2.urlopen("http://www.imdbapi.com/?t=" + movieName)
		data = "[" + page.readlines()[0] + "]"
		obj = json.loads(data)
		if (len(obj) > 1):
			return -1;
		else:
			return float(obj[0]["Rating"])
	except:
		return -1

def clean(name):
	return urllib.quote(re.sub(r'\([^)]*\)', '', name.strip().replace("."," ")))

def getMovieNames(folder):
	lst = os.listdir(folder)
	return map(lambda x:urllib.quote(x), lst)

def process(folder):
	return sorted(map(lambda x:[x, getScore(x)], getMovieNames(folder)), key=itemgetter(1))

results = process("E:\[MOVIES]\[UNSORTED]")

for r in results:
	print (str(r[1]) + "\t" + str(r[0]))