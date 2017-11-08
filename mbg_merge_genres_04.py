# mbg_merge_genres_04.py
# Version a04
# by jmg - jmg*AT*phasechange*DOT*co*DOT*uk
# Nov 8th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Uses artist list `data/mb_alternates.txt'

# Import packages
import os
import resource
from datetime import datetime

# deal with unicode error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

versionNumber = ("a04")
appName = ("mbg_merge_genres_")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# Create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
	os.makedirs("logs")

# Create 'results' subdirectories if necessary
if not os.path.exists("results"):
	os.makedirs("results")

# Open file for writing log
logPath = os.path.join("logs", appName + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Begin
print ('\n' + "Merge MB Genre Alternates | " + appName + " | Version " + versionNumber)
runLog.write ("==========================================================================" + '\n' + '\n')
runLog.write ("Merge MB Genre Alternates | " + appName + " | Version " + versionNumber + '\n' + '\n')

# Get input and process
altInputPath = os.path.join("data", 'mb_alternates.txt')
altInputFile = open (altInputPath, 'r').readlines()

genreFiles = os.listdir("genres")
altList = []

# DO THE THING
for line in altInputFile:
	
	# read line, split, and make list from artists tags
	finalName, alt01, alt02, alt03, alt04, alt05, alt06, alt07, alt08, alt09, alt10, alt11, alt12 = line.split(",")

	finalName = finalName.replace(".","__")
	alt01 = alt01.replace(".","__")
	alt02 = alt02.replace(".","__")
	alt03 = alt03.replace(".","__")
	alt04 = alt04.replace(".","__")
	alt05 = alt05.replace(".","__")
	alt06 = alt06.replace(".","__")
	alt07 = alt07.replace(".","__")
	alt08 = alt08.replace(".","__")
	alt09 = alt09.replace(".","__")
	alt10 = alt10.replace(".","__")
	alt11 = alt11.replace(".","__")
	alt12 = alt12.replace(".","__").replace('\n','')

	# Check genre files and merge alts with finalName
	for index in range(len(genreFiles)):
		genrePath = os.path.join("genres", genreFiles[index])
		openAltGenre = open(genrePath, 'r').readlines()
		genreFile = str(genreFiles[index]).replace(".","__").replace("__txt",".txt")
		genreName, fileExtension = genreFile.split(".")

		print ("Genre name is " + genreName)

		if (genreName == alt01) or (genreName == alt02) or (genreName == alt03) or (genreName == alt04) or (genreName == alt05) or (genreName == alt06) or (genreName == alt07) or (genreName == alt08) or (genreName == alt09) or (genreName == alt10) or (genreName == alt11) or (genreName == alt12):
			# copy file content into finalName
			finalNamePath = os.path.join("genres", finalName + '.txt')
			finalNameFile = open(finalNamePath, 'a')
			for line in openAltGenre:
				finalNameFile.write(line)

			print ("Appended " + genreName + " onto " + finalName)
			runLog.write("Appended " + genreName + " onto " + finalName + '\n')
			altList.append(genreName)

		else:
			# do nothing
			print ("Genre name doesn't match an alt from this line.")

# Delete Alt-genres
deletedAltsCounter = 0
genreFiles = os.listdir("genres")
for index in range(len(genreFiles)):
	genrePath = os.path.join("genres", genreFiles[index])
	genreFile = str(genreFiles[index]).replace(".","__").replace("__txt",".txt")
	genreName, fileExtension = genreFile.split(".")

	if genreName in altList:
		os.remove(genrePath)
		print ("Deleted alt-genre " + genreName)
		runLog.write ("Deleted alt-genre " + genreName + '\n')
		deletedAltsCounter += 1

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

# End timing of run
endTime = datetime.now()
print
print ("Alts deleted: " + str(deletedAltsCounter))
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
runLog.write ("Alts deleted: " + str(deletedAltsCounter) + '\n')
runLog.write ('\n' + 'Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.close()
