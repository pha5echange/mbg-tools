# mb_timeslicer_01.py
# Version a01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# Nov 8th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Generates NEW genre files for each time-category to facilitate processing by existing methods

# Generates OmegaYears from 'data/first_clusters.txt'
# Examines MB genre files and rewrites post-timeslice (to 'ts_data/omegaYear/genres')
# Writes new artist numbers files based upon Omega Year of graph (to 'ts_data/omegaYear')

# Run AFTER 'mbg_merge_genres.py' and 'mb_cluster.py'

# import packages
import os
from collections import OrderedDict

versionNumber = ("a01")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'data' subdirectory if necessary
if not os.path.exists("ts_data"):
    os.makedirs("ts_data")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", 'mb_timeslicer_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Generate dictionary containing nodenames and dates (from 'data\first_cluster.txt')
dateInputPath = os.path.join("data", 'first_cluster.txt')
dateInput = open(dateInputPath, 'r')

dateDict = {}
dateList = []

for line in dateInput:
	genreInput, genreDate, newline = line.split(",")
	genreName = str(genreInput).replace(" ", "")
	dateDict[genreName] = genreDate
	# dateList.append(genreDate)

sortDates = OrderedDict(sorted(dateDict.items()))

for key, value in sortDates.iteritems():
	dateList.append(int(value))

dateSet = set(dateList)

# add 2015 to 'dateSet' 
dateSet.add(2015)

print ('\n' + 'MB Artist Time-Slicer | ' + 'Version: ' + versionNumber + '\n')
runLog.write ('MB Artist Time-Slicer | ' + 'Version: ' + versionNumber + '\n' + '\n')

# Get user input
#print
#dateIP = int(input ("Enter an Omega Year to remove artists that appear AFTER this date (or 2016 to leave data intact): "))
#omegaYear = str(dateIP)

print ('\n' + "Dateset: " + str(dateSet) + '\n')
print ("DateSet elements: " + str(len(dateSet)) + '\n' + '\n')
runLog.write ('\n' + "Dateset: " + str(dateSet) + '\n')
runLog.write("DateSet elements: " + str(len(dateSet)) + '\n' + '\n')

for date in dateSet:

	emptyGenres = 0
	removedGenres = []
	dateIP = int(date)
	omegaYear = str(dateIP)

	# create 'omega year' paths and subdirectories if necessary
	omegaPath = str("ts_data/" + omegaYear)
	if not os.path.exists(omegaPath):
	    os.makedirs(omegaPath)

	omegaGenrePath = str("ts_data/" + omegaYear + "/genres")
	if not os.path.exists(omegaGenrePath):
		os.makedirs(omegaGenrePath)

	# New Artist numbers file
	newArtistNumsPath = os.path.join("ts_data", omegaYear, omegaYear + '_artistNums.txt')
	newArtistNums = open(newArtistNumsPath, 'w')
	newArtistNums.write("Genre" + ',' + "Artists" + '\n')

	# ..and begin..

	print('\n' + "Omega Year: " + omegaYear + '\n')
	runLog.write('\n' + "Omega Year: " + omegaYear + '\n')

	# open files for reading
	for index in range(len(fileNames)):

		artistCounter = 0

		# look for files in 'genres' subfolder
		pathname = os.path.join("genres", fileNames[index])
		genreFile = str(fileNames[index])
		genreLabel, fileExtension = genreFile.split(".")
		dataInput = open(pathname, "r")

		# New genre file
		newGenrePath = os.path.join("ts_data", omegaYear, "genres", omegaYear + '_' + genreLabel + '.txt')
		newGenreFile = open(newGenrePath, 'w')
		
		for line in dataInput:

			# split line and append genreDates' with start date values
			mbid, start, country = line.split("^")
			startDate = int(start)

			if dateIP != 0:
				if startDate <= dateIP:		
					newGenreFile.write(str(mbid) + ',' + str(start) + ',' + str(country))
					artistCounter += 1

		if artistCounter != 0:
			print("In " + omegaYear + " the genre " + genreLabel + " had " + str(artistCounter) + " artist(s)." + '\n')
			runLog.write("In " + omegaYear + " the genre " + genreLabel + " had " + str(artistCounter) + " artist(s)." + '\n')

		# close input files
		dataInput.close()
		newGenreFile.close()

		if os.stat(newGenrePath).st_size == 0:
			os.remove(newGenrePath)
			emptyGenres += 1
			print('In ' + omegaYear + ' the genre ' + genreLabel + ' had no artists. The file has been removed. ' + '\n')
			runLog.write('In ' + omegaYear + ' the genre ' + genreLabel + ' had no artists. The file has been removed. ' + '\n')
			removedGenres.append(genreLabel)

		if artistCounter != 0:
			newArtistNums.write(omegaYear + '_' + genreLabel + ',' + str(artistCounter) + ',' + '\n')

	newArtistNums.close()

	runLog.write ('\n' + 'Removed Genres: ' + str(removedGenres) + '\n')
	runLog.write ('Empty genres: ' + str(emptyGenres) + '\n')
	print ('\n' + 'Removed Genres: ' + str(removedGenres))
	print ('Empty genres: ' + str(emptyGenres))

# write results of run to log file
runLog.write ('\n' + 'Run Information' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.close ()

# write results of run to screen
print ('\n' + 'Run Information')
print ('Version: ' + versionNumber)
