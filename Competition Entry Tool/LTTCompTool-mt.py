import httplib
httplib.HTTPConnection.debuglevel = 1 
import urllib2
import os
from HTMLParser import HTMLParser
import time
import datetime
import threading
parser = HTMLParser()

def getPageNum(source, num):
	url = source+"page-" + str(num);
	request = urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'+url)
	opener = urllib2.build_opener()
	page = opener.open(request) 
	# Read from the object, storing the page's contents in 's'.
	downloadedpage = page.read()
	page.close()
	return downloadedpage

def getNames(downloadedpage):
	namelist = []
	linkstart = 0;
	while(linkstart != -1):
		linkstart = downloadedpage.find("<div itemscope itemtype=\"http://schema.org/Person\" class='user_details'>", linkstart);
		if (linkstart != -1):
			linkend = downloadedpage.find("</span>", linkstart+109);
			linkfragment = downloadedpage[linkstart+109:linkend];
			namelist.append(linkfragment);
			linkstart = linkend
	return namelist

def getPageCount(source):
	page = getPageNum(source, 1)
	pageNumStart = page.find("<meta name=\"description\" content=\"Page")
	pageNumStart = page.find("of", pageNumStart)
	pageNumEnd = page.find(" -", pageNumStart)
	pageTotal = int(page[pageNumStart+3:pageNumEnd])
	print(str(pageTotal) + " Pages")
	return pageTotal

def getPages(source, pageCount):
	pageList = range(1, pageCount+1)
	for pageNum in pageList:
		pageList[pageNum-1] = getPageNum(source, pageNum)
	return pageList

source = raw_input("Enter first page of giveaway: ")
outputname = raw_input("Enter output filename: ")
f = open(outputname, 'w');
counter = 0

seenNames = set();
currentTime = datetime.datetime.now()
start_total_unix_time = time.mktime(currentTime.timetuple())
f.write("Linus Tech Tips Competition Entries\n")
pageTotal = 10
lastPercent = 1;
peopleUnder20posts = 0;
peopleWith1post = 0;
duplicateEntriesFound = 0;
totalPostCount = 0;

for page in getPages(source, getPageCount(source)):
	for name in getNames(page):
		counter += 1;
		if(name in seenNames):
			f.write("Entry:\t" + str(counter) + "\tName:\t" + name + " (Duplicate Entry)" + "\n")
			duplicateEntriesFound += 1;
		else:
			f.write("Entry:\t" + str(counter) + "\tName:\t" + name + "\n")
		seenNames.add(name)

#Prints statistics at the end
f.write("Number of duplicate entries found: " + str(duplicateEntriesFound) + "\n")
currentTime = datetime.datetime.now()
end_total_unix_time = time.mktime(currentTime.timetuple())
timetaken = end_total_unix_time - start_total_unix_time
print("Found " + str(counter) + " entries in " + str(timetaken) + " second/s.");
f.write("Found " + str(counter) + " entries in " + str(timetaken) + " second/s.")
f.close()
foo = raw_input("Press enter to exit...")
