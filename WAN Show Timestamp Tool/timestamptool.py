import time
import datetime

f = open("timestamp.txt", 'w+')
f.write("WAN Show Timestamps:\n")
starttime = datetime.datetime.now()
f.write("The show started at " + str(starttime.hour) + ":" + str(starttime.minute) + "\n")
start_unix_time = time.mktime(starttime.timetuple())
latesttimestamp = "";
while latesttimestamp != "END":
	latesttimestamp = raw_input("Enter new topic title: ")
	currenttime = datetime.datetime.now()
	current_unix_time = time.mktime(currenttime.timetuple())
	timefromstart = int(current_unix_time - start_unix_time)
	hours = int(timefromstart/(60*60))
	minutes = int((timefromstart-(hours*60*60))/60)
	seconds = int(timefromstart-((hours*60*60)+(minutes*60)))
	hours = str(hours)
	if len(hours) == 1:
		hours = "0" + hours
	minutes = str(minutes)
	if len(minutes) == 1:
		minutes = "0" + minutes
	seconds = str(seconds)
	if len(seconds) == 1:
		seconds = "0" + seconds
	f.write(hours + ":" + str(minutes) + ":" + str(seconds) + " - " + str(latesttimestamp) + "\n");
	f.flush();
f.close();
