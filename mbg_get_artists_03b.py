# mbg_get_artists_03b.py
# Version a03b
# by jmg - jmg*AT*phasechange*DOT*co*DOT*uk
# June 29th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Fetches artists from MusicBrainz (based upon the Echo Nest artists)
# Writes name, ID and type to `results/mb_artists.txt'
# Depends upon `data/en_mb_map.txt' for input (`NAME ^ ENID ^ MBID')

# Import packages
import os
import resource
import musicbrainzngs
from datetime import datetime

# deal with unicode error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

versionNumber = ("a03b")

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
logPath = os.path.join("logs", 'mbg_get_artists_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Begin
print ('\n' + "MusicBrainz Get Artists | Version " + versionNumber)
runLog.write ("==========================================================================" + '\n' + '\n')
runLog.write ("MusicBrainz Get Artists | Version " + versionNumber + '\n' + '\n')

# Open file for writing results
resultsPath = os.path.join("results", 'mb_artists_' + versionNumber + '.txt')
resultsFile = open(resultsPath, 'w')

# Set MusicBrainz rate limit and useragent
musicbrainzngs.set_rate_limit(limit_or_interval=1.0, new_requests=1)
musicbrainzngs.set_useragent(
	"MusicBrainz Genre Tools",
	"0.1",
	"http://www.phasechange.info/mbgtools/index.htm",
)

artistCounter = 0
notFoundCounter = 0

# Get input and process
idInputPath = os.path.join("data", 'en_mb_map.txt')
idInput = open (idInputPath, 'r').readlines()

# Get artist IDs from input file, and interrogate MusicBrainz for each
for line in idInput:
	artistName, enId, mbId = line.split("^")
	cleanMbId = str(mbId).replace('\n','').replace('\r','')
	cleanArtistName = str(artistName).replace('"', "'")

	try:
		result = musicbrainzngs.get_artist_by_id(mbId, includes=["aliases"])
		artistCounter += 1
	except:
		try:
			result = musicbrainzngs.get_artist_by_id(mbId)
			artistCounter += 1
		except:
			cleanMbArtist = ("NOT FOUND - " + cleanArtistName)
			resultsFile.write (cleanMbArtist + "^" + cleanMbId + "^" + '\n')
			notFoundCounter += 1
			pass
		else:
			artist = result["artist"]
			cleanMbArtist = str(artist["name"]).replace('"', "'")

			try:
				print ('\n' + "Name: " + cleanMbArtist)
			except:
				pass

			try:
				print ("MBID: " + cleanMbId)
			except:
				pass

			try:
				print ("Type:" + artist["type"])
			except:
				pass

			try:
				resultsFile.write (cleanMbArtist + "^" + cleanMbId + "^" + artist["type"] + '\n')
			except:
				resultsFile.write (cleanMbArtist + "^" + cleanMbId + "^" + '\n')

	print str(result)		

resultsFile.close()

# End timing of run
endTime = datetime.now()
print
print ("Complete.")
print ("Artist Count: " + str(artistCounter))
print ("Unfound Artists: " + str(notFoundCounter))
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
runLog.write ("Artist Count: " + str(artistCounter) + '\n')
runLog.write("Unfound Artists: " + str(notFoundCounter) + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')

runLog.close()
