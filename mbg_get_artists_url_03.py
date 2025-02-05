# mbg_get_artists_url_03.py
# Version a03
# by jmg - jmg*AT*phasechange*DOT*co*DOT*uk
# July 6th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Fetches artists from MusicBrainz (based upon the Echo Nest artists)
# Writes XML to `results/mb_artists_mbg_get_artists_url.txt'
# Depends upon `data/en_mb_map.txt' for input (`NAME ^ ENID ^ MBID')
# URL-requests version
# Time-sliced artist lists catered for in this version

# Import packages
import os
import resource
import requests
from datetime import datetime
from time import sleep

# deal with unicode error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

versionNumber = ("a03")
appName = ("mbg_get_artists_url_")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# Create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
	os.makedirs("logs")

# Create 'data' subdirectories if necessary
if not os.path.exists("data"):
	os.makedirs("data")

# Create 'results' subdirectories if necessary
if not os.path.exists("results"):
	os.makedirs("results")

# Open file for writing log
logPath = os.path.join("logs", appName + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Begin
print ('\n' + "MusicBrainz Get Artists | " + appName + " | Version " + versionNumber)
runLog.write ("==========================================================================" + '\n' + '\n')
runLog.write ("MusicBrainz Get Artists | " + appName + " | Version " + versionNumber + '\n' + '\n')

# Get user input
dateIP = int(input("Enter an Omega Year to use time-sliced mapping (or 0 to use the full map): "))
omegaYear = str(dateIP)

# Open file for writing results
if dateIP == 0:
	resultsPath = os.path.join("results", 'mb_artists_' + appName + versionNumber + '.txt')
else:
	resultsPath = os.path.join("results", omegaYear + '_mb_artists_' + appName + versionNumber + '.txt')

resultsFile = open(resultsPath, 'w')

# Get input and process
if dateIP == 0:
	idInputPath = os.path.join("data", 'en_mb_map.txt')
	idInput = open (idInputPath, 'r').readlines()
else:
	idInputPath = os.path.join("data", omegaYear + '_en_mb_map.txt')
	idInput = open (idInputPath, 'r').readlines()

# Get artist IDs from input file, and interrogate MusicBrainz for each
for line in idInput:
	artistName, enId, mbId = line.split("^")
	cleanMbId = str(mbId).replace('\n','').replace('\r','')
	mbUrl = ("https://musicbrainz.org/ws/2/artist/" + cleanMbId + "?inc=tags")

	try:
		sleep(1)
		result = requests.get(mbUrl)
	except:
		pass

	try:
		print
		print result.content
		print
		resultsFile.write(str(result.content) + '\n')
	except:
		pass

resultsFile.close()

# End timing of run
endTime = datetime.now()
print
print ("Complete.")
print ("Omega Year: " + omegaYear)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
runLog.write ("Omega Year: " + omegaYear + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')

runLog.close()
