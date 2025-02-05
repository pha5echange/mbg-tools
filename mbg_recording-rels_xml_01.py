# mbg_recording-rels_xml_01.py
# Version a01
# by jmg - jmg*AT*phasechange*DOT*co*DOT*uk
# July 31st 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Processes XML file `results/mb_artists_mbg_get_artists_url.txt'
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

versionNumber = ("a01")
appName = ("mbg_recording-rels_xml_")
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
print ('\n' + "Process MusicBrainz Recording Relations XML | " + appName + " | Version " + versionNumber)
runLog.write ("==========================================================================" + '\n' + '\n')
runLog.write ("Process MusicBrainz Recording Relations XML | " + appName + " | Version " + versionNumber + '\n' + '\n')

# Open file for writing results
resultsPath = os.path.join("results", 'mb_recording-rels_xml_' + versionNumber + '.txt')
resultsFile = open(resultsPath, 'w')

# Get input and process
xmlInputPath = os.path.join("results", 'mbg_get_artists_url_RECORDING-RELS.txt')
xmlInput = open (xmlInputPath, 'r').readlines()

# Read XML file (ignoring empty lines) and process
lineCounter = 0

for line in xmlInput:
	lineCounter += 1

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
	relations = []
	del relations [:]
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

	for elem in tree.iterfind('artist/relation-list/relation[@type="producer"]/target'): 
		print ('\n' + "tree.iterfind('artist/relation-list/relation[@type='producer']/target'): ")
		print >> runLog, '\n' + "tree.iterfind('artist/relation-list/relation[@type='producer']/target'): "
		print elem.tag, elem.attrib, elem.text
		print >> runLog, elem.tag, elem.attrib, elem.text
		relation = str(elem.text)
		relations.append(relation)

	resultsFile.write(artistID + '^' + artistType + '^' + artistBegin + '^' + artistCountry + '^' + str(relations) + '\n')

resultsFile.close()

# Remove duplicates
cleanLineCounter = 0
lines = open(resultsPath, 'r').readlines()
lines_set = set(lines)
out = open(resultsPath, 'w')

for line in sorted(lines_set):
	out.write(line)
	cleanLineCounter +=1

# End timing of run
endTime = datetime.now()
print
print ("Complete.")
print ("Lines processed: " + str(lineCounter))
print ("Lines written: " + str(cleanLineCounter))
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
runLog.write ('\n' + "Lines processed: " + str(lineCounter) + '\n')
runLog.write ("Lines written: " + str(cleanLineCounter) + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')

runLog.close()
