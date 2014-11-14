import httplib
httplib.HTTPConnection.debuglevel = 1 
import urllib2
import os
from HTMLParser import HTMLParser
import time
import datetime
parser = HTMLParser()

f = open('sourcefile.txt', 'r')
sourceArray = []
for line in f:
	sourceArray.append(line)
f.close();
f = open('formatedfile.html', 'w');
f.write("<html><meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\" />")
counter = 0
currentTime = datetime.datetime.now()
start_total_unix_time = time.mktime(currentTime.timetuple())
print("Completed:")
errors = "";
for url in sourceArray:
	if("linustechtips.com" not in url):
		errors += "Not linustechtips: " + url + "<br>";
		print ("Not linustechtips: " + url + "\n")
		continue;
	currentTime = datetime.datetime.now()
	start_unix_time = time.mktime(currentTime.timetuple())
	counter += 1
	try:
		request = urllib2.Request(url)
		request.add_header('User-Agent', 'OpenAnything/1.0+'+url)
		opener = urllib2.build_opener()
		page = opener.open(request)	
		# Read from the object, storing the page's contents in 's'.
		downloadedpage = page.read()
		page.close()
	except:
		errors += "Error loading: " + url + "<br>";
		print ("Error loading: " + url + "\n")
		continue;
	#f.write(downloadedpage)
	indexOfStart = downloadedpage.find("<meta property=\"og:title\" content=")
	if indexOfStart != (-1):
		indexOfEnd = downloadedpage.find("\"/>", indexOfStart)
		if indexOfEnd == (-1):
			print("Error finding end of title in url:\t" + url)
			exit(5);
	#extractedTitle = parser.unescape(downloadedpage[indexOfStart+35: indexOfEnd])
	extractedTitle = downloadedpage[indexOfStart+35: indexOfEnd]
	extractedTitle = (extractedTitle[:extractedTitle.find("- Tech News and Reviews")]).title()
	#stringToWrite = "Topic "+ str(counter) + "\n" + extractedTitle + "\nSource 1: linustechtips.com "
	if (url[-1] != '/'):
		url = url[:-1]
	stringToWrite = "<h2>" + extractedTitle + "</h2>\nSource 1: <a href=\"" + url + "\">linustechtips.com</a>"
	
	
	#<link rel='author' href='http://linustechtips.com/main/user/82552-ren/' />
	indexOfStart = downloadedpage.find("<link rel='author' href=")
	if indexOfStart != (-1):
		indexOfEnd = downloadedpage.find("/>", indexOfStart)
		if indexOfEnd == (-1):
			print("Error finding end of title in url:\t" + url)
			exit(5);
	# cut out the string with the OP plus the user number
	op = downloadedpage[indexOfStart+60: indexOfEnd-3]
	# cut off the user number
	op = op[op.find("-")+1:]
	op = op.replace("-", " ")
	# uppercase all words
	op = op.title()
	stringToWrite += " OP: <a href=\"" + downloadedpage[indexOfStart+25: indexOfEnd-3] +"\">" + op + "</a>\n"
	# crawl opening post for links
	indexOfStart = downloadedpage.find("<div itemprop=\"commentText\" class='post entry-content '>")
	if indexOfStart != (-1):
		foundEnd = False
		tempIndexOfStart = indexOfStart
		while(foundEnd == False):
			indexOfEnd = downloadedpage.find("</div>", tempIndexOfStart)
			indexOfNewTag = downloadedpage.find("<div>", tempIndexOfStart, indexOfEnd)
			if (indexOfNewTag != -1):
				tempIndexOfStart = indexOfEnd+4
				#f.write("I was here<br>")
				continue
			else:
				#f.write("I was here2<br>")
				foundEnd = True
			if indexOfEnd == (-1):
				print("Error finding end of title in url:\t" + url)
				exit(5);
	openingpost = downloadedpage[indexOfStart:indexOfEnd]
	linkstart = 0;
	linklist = []
	while(linkstart != -1):
		linkstart = openingpost.find("<a href=", linkstart);	
		if (linkstart != -1):
			linkend = openingpost.find(openingpost[linkstart+8], linkstart+9);
			linkfragment = openingpost[linkstart+9:linkend];
			linklist.append(linkfragment);
			linkstart = linkend
	linkcounter = 1
	linklist = list(set(linklist));
	for link in linklist:
		linkcounter +=1
		shortlinkbegin = 0;
		templink = link[link.find("://")+3:]
		tempnum = templink.find("www.");
		if (tempnum != -1):
			templink = templink[4:]
		templink = templink[:templink.find("/")]
		stringToWrite += "\n<br>Source " + str(linkcounter) + ": <a href=\"" + link + "\">" + templink + "</a>"
#Create a printout to console to show the time taken
	currentTime = datetime.datetime.now()
	end_unix_time = time.mktime(currentTime.timetuple())
	timeTaken = end_unix_time - start_unix_time;
	if(len(extractedTitle) > 60):
		extractedTitle = extractedTitle[:60]
	print(extractedTitle +" in "+ str(timeTaken) + " second/s");
	f.write(stringToWrite+"\n<br>&lt;body&gt\n\n")
f.write("<h2>Errors</h2><p>" + errors + "</p>")
f.write("</html>")
f.close()
currentTime = datetime.datetime.now()
end_total_unix_time = time.mktime(currentTime.timetuple())
timetaken = end_total_unix_time - start_total_unix_time
print("Time taken to compile " + str(len(sourceArray)) + " source/s: " + str(timetaken) + " second/s.\nPress any enter to exit...");
input()
	
	
