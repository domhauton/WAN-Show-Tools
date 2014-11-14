import httplib
httplib.HTTPConnection.debuglevel = 1 
import urllib2
import os
from HTMLParser import HTMLParser
import time
import datetime
parser = HTMLParser()

source = raw_input("Enter first page of giveaway: ")
outputname = raw_input("Enter output filename: ")
f = open(outputname, 'w');
counter = 0
pageCounter = 0;
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
while True:
	pageCounter += 1
	if pageCounter > pageTotal:
		break
	url = source+"page-" + str(pageCounter);
	request = urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'+url)
	opener = urllib2.build_opener()
	page = opener.open(request) 
	# Read from the object, storing the page's contents in 's'.
	downloadedpage = page.read()
	page.close()
	if (pageCounter == 1):
		pageNumStart = downloadedpage.find("<meta name=\"description\" content=\"Page")
		pageNumStart = downloadedpage.find("of", pageNumStart)
		pageNumEnd = downloadedpage.find(" -", pageNumStart)
		pageTotal = int(downloadedpage[pageNumStart+3:pageNumEnd])
		print(str(pageTotal) + " Pages")
	else:
		if (pageCounter > (pageTotal/20)*lastPercent):
			print(str(lastPercent*5) + "% Completed " + str(counter) + " Entries");
			lastPercent+=1;
	namelist = []
	linkstart = 0;
	#f.write(downloadedpage)
	while(linkstart != -1):
		linkstart = downloadedpage.find("<div itemscope itemtype=\"http://schema.org/Person\" class='user_details'>", linkstart);
		#counter += 1
		if (linkstart != -1):
			linkend = downloadedpage.find("</span>", linkstart+109);
			linkfragment = downloadedpage[linkstart+109:linkend];
			namelist.append(linkfragment);
			linkstart = linkend
			linkstart = downloadedpage.find("<li class='post_count desc lighter'>", linkstart);
			linkend = downloadedpage.find(" post", linkstart+36)
			linkfragment = downloadedpage[linkstart+36:linkend]
			linkfragment = linkfragment.replace(",", "")
			if int(linkfragment) == 1:
				peopleWith1post += 1;
			if int(linkfragment) < 20:
				peopleUnder20posts += 1
			totalPostCount += int(linkfragment)
			linkstart = linkend
			#counter +=1
	for name in namelist:
		counter += 1;
		if(name in seenNames):
			f.write("Entry:\t" + str(counter) + "\tName:\t" + name + " (Duplicate Entry)" + "\n")
			duplicateEntriesFound += 1;
		else:
			f.write("Entry:\t" + str(counter) + "\tName:\t" + name + "\n")
		seenNames.add(name)
f.write("Number of entries with 1 post: " + str(peopleWith1post) + "\n")
f.write("Number of entries with <20 posts: " + str(peopleUnder20posts) + "\n")
if(counter > 0):
	f.write("Average post count: " + str(totalPostCount/counter) + "\n")
	print("Average post count: " + str(totalPostCount/counter))
f.write("Number of duplicate entries found: " + str(duplicateEntriesFound) + "\n")
print("Number of entries with 1 post: " + str(peopleWith1post))
print("Number of entries with <20 posts: " + str(peopleUnder20posts))
print("Number of duplicate entries found: " + str(duplicateEntriesFound))
currentTime = datetime.datetime.now()
end_total_unix_time = time.mktime(currentTime.timetuple())
timetaken = end_total_unix_time - start_total_unix_time
print("Found " + str(counter) + " entries in " + str(timetaken) + " second/s.");
f.write("Found " + str(counter) + " entries in " + str(timetaken) + " second/s.")
f.close()
foo = raw_input("Press enter to exit...")
