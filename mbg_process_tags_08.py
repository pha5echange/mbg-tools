# mbg_process_tags_08.py
# Version a08
# by jmg - jmg*AT*phasechange*DOT*co*DOT*uk
# Nov 7th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Uses artist list `data/artist_list.txt' and `data/user_tag_list.txt'
# Finds artists with genre tags
# Writes results to `results/mb_tagged_artists.txt', `results/mb_nontagged_artists.txt' and results/mb_tags_used.txt'
# Writes genres/artistLists
# This version fixes artist start dates al-la 'eng_MBdate', then re-sorts files by date

# Import packages
import os
import resource
from datetime import datetime

# deal with unicode error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

versionNumber = ("a08")
appName = ("mbg_process_tags_")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# Create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
	os.makedirs("logs")

# create 'genres' subdirectory if necessary
if not os.path.exists("genres"):
    os.makedirs("genres")

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
print
runLog.write ("Tags Input: " + '\n')
runLog.write (str(tagsInput) + '\n' + '\n')

cleanTagsInput = []
del cleanTagsInput[:]
cleanTagCounter = 0

for item in tagsInput:
	item = item.replace("\n","").replace('/','_').replace(' ','')
	cleanTagsInput.append(item)
	cleanTagCounter += 1

print
print("Clean Tags Input: ")
print(str(cleanTagsInput))
print
runLog.write ("Clean Tags Input: " + '\n')
runLog.write (str(cleanTagsInput) + '\n' + '\n')

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

	# Fix date
	if not artistBegin:
		strChars = 0
	else:
		strChars = len(artistBegin)
		artistBegin = artistBegin[:4]
		if artistBegin == "????":
			strChars = 0
		else:
			try:
				beginInt = int(artistBegin)
			except:
				pass

	# Fix up dates for `Person'
	if artistType == "Person":
		try:
			if strChars > 4:
				personBegin = beginInt + 20
				# Deal with those born less than 20 years ago
				if personBegin >= 2017:
					personBegin = 2015
			else:
				personBegin = beginInt

			artistBegin = str(personBegin)
		except:
			pass

	print
	print ("New Artist")
	print
	print("tagNames: ")
	print (str(tagNames))
	runLog.write ('\n' + "New Artist" + '\n')
	runLog.write ("tagNames: " + '\n')
	runLog.write (str(tagNames) + '\n' + '\n')

	cleanTagNames = tagNames.replace("\n","").replace(' ','').replace('/','_').replace("'","")
	artistTags = cleanTagNames.split(",")

	print("artistTags: ")
	print (str(artistTags))
	runLog.write ("artistTags: " + '\n')
	runLog.write (str(artistTags) + '\n' + '\n')

	for item in artistTags:
		item = item.strip().replace("[","").replace("]","").replace('"','').replace(",","") 
		print
		print("Item: ")
		print(str(item))

		if item in cleanTagsInput:
			newArtistTags.append(item)
			tagsListFile.write(item + '\n')
			genreName = str(item)
			genresPath = os.path.join("genres", genreName + '.txt')
			genreArtistList = open(genresPath, 'a')
			genreArtistList.write(artistID + '^' + artistBegin + '^' + artistCountry + '\n')
			print("Added " + artistCountry + " artist to " + genreName + " file.")
			runLog.write ("Added " + artistID + " from " + artistCountry + " to " + genreName + " file." + '\n')

	if newArtistTags:
		# Write resultsFile
		resultsFile.write(cleanOrigID + '^' + artistID + '^' + artistType + '^' + artistBegin + '^' + artistCountry + '^' + str(newArtistTags) + '\n')
		taggedArtistCounter += 1
		print("Artist written to taggedArtists file.")
		runLog.write (artistID + " written to taggedArtists file." + '\n')
	else:
		noTagsFile.write(cleanOrigID + '^' + artistID + '^' + artistType + '^' + artistBegin + '^' + artistCountry + '^' + str(tagNames) + '\n')
		nonTaggedCounter += 1
		print("No artist tags. Artist written to noTags file.")
		runLog.write ("No artist tags for artist " + artistID + ". Written to noTags file." + '\n')

resultsFile.close()
noTagsFile.close()
tagsListFile.close()
genreArtistList.close()

# Remove duplicates in genre files
cleanGenresCounter = 0
genreFiles = os.listdir("genres")
for index in range(len(genreFiles)):
	genrePath = os.path.join("genres", genreFiles[index])

	lines = open(genrePath, 'r').readlines()
	lines_set = set(lines)
	out = open(genrePath, 'w')

	for line in sorted(lines_set):
		out.write(line)
		cleanGenresCounter += 1

# Re-sort genre files by new start dates
datedFiles = os.listdir("genres")

for index in range(len(datedFiles)):
	datedPath = os.path.join("genres", datedFiles[index])
	sortedFile = sorted(open(datedPath).readlines(), key=lambda line: int(line.split('^')[1]))
	out = open(datedPath, 'w')

	for line in sortedFile:
		out.write(line)

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
