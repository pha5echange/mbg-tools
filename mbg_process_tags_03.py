# mbg_process_tags_03.py
# Version a03
# by jmg - jmg*AT*phasechange*DOT*co*DOT*uk
# Oct 27th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Uses artist list `data/artist_list.txt' and `data/user_tag_list.txt'
# Finds artists with genre tags
# Writes results to `results/mb_tagged_artists.txt' and `results/mb_nontagged_artists.txt'

# Import packages
import os
import resource
from datetime import datetime

# deal with unicode error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

versionNumber = ("a03")
appName = ("mbg_process_tags_")

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
print ('\n' + "Process MusicBrainz Tags | " + appName + " | Version " + versionNumber)
runLog.write ("==========================================================================" + '\n' + '\n')
runLog.write ("Process MusicBrainz Tags | " + appName + " | Version " + versionNumber + '\n' + '\n')

# Open files for writing results
resultsPath = os.path.join("results", 'mb_tagged_artists_' + versionNumber + '.txt')
resultsFile = open(resultsPath, 'w')

noTagsPath = os.path.join("results", 'mb_nontagged_artists_' + versionNumber + '.txt')
noTagsFile = open(noTagsPath, 'w')

tagsListPath = os.path.join("results", 'mb_tags_used_' + versionNumber + '.txt')
tagsListFile = open(tagsListPath, 'w')

# Get input and process
artistsInputPath = os.path.join("data", 'artist_list.txt')
artistsInput = open (artistsInputPath, 'r').readlines()

tagsInputPath = os.path.join("data", 'user_tag_list.txt')
tagsInput = open (tagsInputPath, 'r').readlines()

print("Tags Input: ")
print(str(tagsInput))

cleanTagsInput = []
del cleanTagsInput[:]

for item in tagsInput:
	item = item.replace("\n","")
	cleanTagsInput.append(item)

print
print("Clean Tags Input: ")
print(str(cleanTagsInput))
print

# DO THE THING
taggedArtistCounter = 0
nonTaggedCounter = 0
for line in artistsInput:
	artistTags = []
	del artistTags[:]
	newArtistTags = []
	del newArtistTags[:]
	
	# read line, split, and make list from artists tags
	cleanOrigID, artistID, artistType, artistBegin,artistCountry, tagNames = line.split("^")

	print("tagNames: ")
	print (str(tagNames))

	artistTags = tagNames.split()

	print("artistTags: ")
	print (str(artistTags))

	for item in artistTags:
		item = item.strip().replace("['","").replace("']","").replace("',","").replace("'","").replace('["','').replace('"]','') 
		print("Item: ")
		print(str(item))
		print
		if item in cleanTagsInput:
			newArtistTags.append(item)
			tagsListFile.write(item + '\n')

	if not newArtistTags:
		noTagsFile.write(cleanOrigID + '^' + artistID + '^' + artistType + '^' + artistBegin + '^' + artistCountry + '^' + str(tagNames) + '\n')
		nonTaggedCounter += 1
	else:
		resultsFile.write(cleanOrigID + '^' + artistID + '^' + artistType + '^' + artistBegin + '^' + artistCountry + '^' + str(newArtistTags) + '\n')
		taggedArtistCounter += 1

resultsFile.close()
noTagsFile.close()

# Remove duplicates in tagsListFile
tagsUsedCounter = 0
lines = open(tagsListPath, 'r').readlines()
lines_set = set(lines)
out = open(tagsListPath, 'w')

for line in sorted(lines_set):
	out.write(line)
	tagsUsedCounter +=1

tagsListFile.close()

# End timing of run
endTime = datetime.now()
print
print ("Complete.")
print ("Tagged Artists: " + str(taggedArtistCounter))
print ("Non-Tagged Artists: " + str(nonTaggedCounter))
print ("Tags used: " + str(tagsUsedCounter))
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
runLog.write ('\n' + "Tagged Artists: " + str(taggedArtistCounter) + '\n')
runLog.write ("Non-Tagged Artists: " + str(nonTaggedCounter) + '\n')
runLog.write ("Tags used: " + str(tagsUsedCounter) + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.close()
