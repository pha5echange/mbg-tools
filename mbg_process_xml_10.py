# mbg_process_xml_10.py
# Version a10
# by jmg - jmg*AT*phasechange*DOT*co*DOT*uk
# Oct 23rd 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Processes XML file `results/mb_artists_mbg_get_artists_url.txt'
# Writes results to `results/mb_artists_xml.txt'
# Processes user-tags and writes to seperate, non-duplicate-line file (`results/mb_artists_tags.txt')
# Gets original MBID's from the en_mb map, to accomodate for id-changes in MB returns
# Removes duplicate lines

# Import packages
import os
import xml.etree.ElementTree as eT
import resource
from datetime import datetime

# deal with unicode error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

versionNumber = ("a10")
appName = ("mbg_process_xml_")
namespace = "{http://musicbrainz.org/ns/mmd-2.0#}"

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

# Define path to tempXML.xml file
tempPath = os.path.join("data", 'tempXML.xml')

# Begin
print ('\n' + "Process MusicBrainz XML | " + appName + " | Version " + versionNumber)
runLog.write ("==========================================================================" + '\n' + '\n')
runLog.write ("Process MusicBrainz XML | " + appName + " | Version " + versionNumber + '\n' + '\n')

# Open files for writing results
resultsPath = os.path.join("results", 'mb_artist_xml_' + versionNumber + '.txt')
resultsFile = open(resultsPath, 'w')

tagsPath = os.path.join("results", 'mb_artist_tags_' + versionNumber + '.txt')
tagsFile = open(tagsPath, 'w')

# Get input and process
xmlInputPath = os.path.join("results", 'mb_artists_mbg_get_artists_url.txt')
xmlInput = open (xmlInputPath, 'r').readlines()

idInputPath = os.path.join("data", 'en_mb_map.txt')
idInput = open (idInputPath, 'r').readlines()

# Read XML file (ignoring empty lines) and process
lineCounter = 0

for line in xmlInput:
	lineCounter += 1

	origIDline = idInput[lineCounter-1]
	origName, enID, origID = origIDline.split("^")
	cleanOrigID = str(origID).replace('\n','').replace('\r','')

	artistID = ""
	artistType = ""
	artistBegin = ""
	artistCountry = ""

	cleanLine = str(line).replace('<metadata xmlns="http://musicbrainz.org/ns/mmd-2.0#">','<metadata>').strip()

	# Open temp xml file, clean and write line to it, then close
	tempXMLFile = open(tempPath, 'w')
	tempXMLFile.write (str(cleanLine))
	tempXMLFile.close()

	# Parse tempXML file
	tree = eT.ElementTree(file='data/tempXML.xml')
	root = tree.getroot()

	# Get the things
	tagNames = []
	del tagNames [:]
	print ('\n' + "Iter method: ")
	print >> runLog, '\n' + "Iter Method: "

	for elem in tree.iter(tag='artist'):
		print ('\n' + "tree.iter (tag='artist'): ")
		print >> runLog, '\n' + "tree.iter (tag='artist'): "

		try:
			artistID = str(elem.attrib['id'])
		except:
			pass

		try:
			artistType = str(elem.attrib['type'])
		except:
			pass

		print elem.tag, artistID, artistType
		print >> runLog, elem.tag, artistID, artistType

	for elem in tree.iter(tag='begin'):
		print ('\n' + "tree.iter (tag='begin'): ")
		print >> runLog, '\n' + "tree.iter (tag='begin'): "
		print elem.tag, elem.attrib, elem.text
		print >> runLog, elem.tag, elem.attrib, elem.text
		artistBegin = str(elem.text)

	for elem in tree.iter(tag='country'):
		print ('\n' + "tree.iter (tag='country'): ")
		print >> runLog, '\n' + "tree.iter (tag='country'): "
		print elem.tag, elem.attrib, elem.text
		print >> runLog, elem.tag, elem.attrib, elem.text
		artistCountry = str(elem.text)

	for elem in tree.iterfind('artist/tag-list/tag/name'): 
		print ('\n' + "tree.iterfind('artist/tag-list/tag/name'): ")
		print >> runLog, '\n' + "tree.iterfind('artist/tag-list/tag/name'): "
		print elem.tag, elem.attrib, elem.text
		print >> runLog, elem.tag, elem.attrib, elem.text
		tagName = str(elem.text)
		tagNames.append(tagName)


	# Write results file
	resultsFile.write(cleanOrigID + '^' + artistID + '^' + artistType + '^' + artistBegin + '^' + artistCountry + '^' + str(tagNames) + '\n')

	# Write tags file
	for item in tagNames:
		tagsFile.write("%s\n" % item)

resultsFile.close()
tagsFile.close()

# Remove duplicates in resultsFile
cleanLineCounter = 0
lines = open(resultsPath, 'r').readlines()
lines_set = set(lines)
out = open(resultsPath, 'w')

for line in sorted(lines_set):
	out.write(line)
	cleanLineCounter +=1

# Remove duplicates in tagsFile
tagLineCounter = 0
lines = open(tagsPath, 'r').readlines()
lines_set = set(lines)
out = open(tagsPath, 'w')

for line in sorted(lines_set):
	out.write(line)
	tagLineCounter +=1

# End timing of run
endTime = datetime.now()
print
print ("Complete.")
print ("Lines processed: " + str(lineCounter))
print ("Lines written: " + str(cleanLineCounter))
print ("Tag-lines written: " + str(tagLineCounter))
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
runLog.write ('\n' + "Lines processed: " + str(lineCounter) + '\n')
runLog.write ("Lines written: " + str(cleanLineCounter) + '\n')
runLog.write("Tag-lines written: " + str(tagLineCounter) + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')

runLog.close()
