import httplib
httplib.HTTPConnection.debuglevel = 1 
import urllib2
import os
from HTMLParser import HTMLParser
import time
import datetime
parser = HTMLParser()

def shortenLink(originalLink, length, flag = True, lencap = 0):
	if(flag):
		length = 5
	length += 1
	shortlinkbegin = 0;
	modifiedLink1 = originalLink[originalLink.find("://")+3:]
	indexOfWWW = modifiedLink1.find("www.");
	if (indexOfWWW != -1):
		modifiedLink1 = modifiedLink1[4:]
	if (len(modifiedLink1) < 68):
		return modifiedLink1
	shortLinkEnd = -1;
	for x in range(0, length):
		shortLinkEndNew = modifiedLink1.find("/", shortLinkEnd+1)
		if shortLinkEndNew == -1:
			shortLinkEndNew = modifiedLink1.find(".html", shortLinkEnd+1)
		if (shortLinkEndNew == -1):
			shortLinkEndNew = len(modifiedLink1)
		if((shortLinkEndNew - shortLinkEnd > 40) & flag):
			base = shortenLink(originalLink, 0, False)
			tail = modifiedLink1[shortLinkEnd+1:shortLinkEndNew]
			if(lencap != 0):
				tail = tail[7:]
			tail = tail.replace("-", " ")
			tail = tail.replace("_", " ")
			baseLen = len(base);
			tailLen = 68 - (baseLen+3+lencap)
			if (tailLen > len(tail)):
				return base + " - " + tail
			return base + " - " + tail[:tailLen]
		if(shortLinkEndNew == -1):
			break
		shortLinkEnd = shortLinkEndNew
	if (shortLinkEnd == -1):
		return modifiedLink1
	return modifiedLink1[:shortLinkEnd]

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
topicCounter = 1
mainLinkCounter = 1
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
	extractedTitle = (extractedTitle[:extractedTitle.find("- Tech News and Reviews")])
	#stringToWrite = "Topic "+ str(counter) + "\n" + extractedTitle + "\nSource 1: linustechtips.com "
	if (url[-1] != '/'):
		url = url[:-1]
	modifiedUrl = shortenLink(url, 3)
	stringToWrite = "<h2>" + extractedTitle + "</h2>Source 1: <a href=\"" + url + "\">" + modifiedUrl + "</a>"
	
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
	
	modifiedUrl = shortenLink(url, 3, True, len(op))
	stringToWrite = "<h2>" + extractedTitle + "</h2>Source 1: <a href=\"" + url + "\">" + modifiedUrl + "</a>"
	
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
	mainLinkCounter = 2
	for link in linklist:
		linkcounter +=1
		templink = shortenLink(link, 2)
		stringToWrite += "\n<br>Source " + str(linkcounter) + ": <a href=\"" + link + "\">" +templink + "</a>"
		mainLinkCounter += 1
	topicCounter += 1;
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
timetaken = float(end_total_unix_time) - float(start_total_unix_time)
print("Time taken to compile " + str(len(sourceArray)) + " source/s: " + str(timetaken) + " second/s.\nPress any enter to exit...");
raw_input()
	
	
