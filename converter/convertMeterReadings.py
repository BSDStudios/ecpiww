#!/usr/bin/env python3
import os
import sys
import getopt

import time as t
import xml.etree.ElementTree as ET

def usage():
    print "\nUsage: python %s -l [FF CamReader XML Log Data]\n" % os.path.basename(sys.argv[0])
    sys.exit(0)

try:
    opts, args = getopt.getopt(sys.argv[1:], "hl:")
    if len(opts) == 0:
        usage()

except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == '-l':
        inFile = opt[1]
    if opt[0] == '-h':
        usage()


#############################
### XML reader
##############################

def XMLparser(XMLecpiLogFile):

  tree = ET.parse(XMLecpiLogFile)
  root = tree.getroot()

# echo
  print "Reading XML log file: %s" % inFile
  for date,reading in zip(tree.iterfind('OCR/Date'),tree.iterfind('OCR/ReadingVal')):
    print date.text, reading.text

# read file
  readingValues = [float(value.text) for value in tree.iterfind('OCR/ReadingVal')]
  readingDates =  readingValues[::-1] #reverse order
  readingDates = [t.strptime(dates.text,'%d.%m.%Y %H:%M:%S') for dates in tree.iterfind('OCR/Date')]
  readingDates = [t.strftime("%Y-%m-%dT%H:%M:%S",dates) for dates in readingDates[::-1]] #reverse order as well

  # prepare data
  consuption = [x - y for x, y in zip(readingValues[1:], readingValues[:-1])]
  # start, end, consuption, reading, reading
  reading = zip(readingDates[:-1],consuption,readingDates[1:],readingValues[:-1],readingValues[1:])

  return reading


#############################
# JSON parser functions
#############################

def JSON_Reading(Reading,Date,Type):
  Reading = {
      "Reading":Reading,
      "AsAt":Date,
      "Type":Type
  }
  return Reading

def JSON_Usages(consuption,DateStart,readingStart,DateEnd,readingEnd,EnergyDescription,meterType):
  Usages = {
    "Period" : {
        "PeriodStart": DateStart,
        "PeriodEnd": DateEnd
    },
    "KwhUsed":consuption,
    "StartReading":JSON_Reading(readingStart,DateStart,meterType),
    "EndtReading": JSON_Reading(readingStart,DateEnd,meterType),
    "EnergyDescription":EnergyDescription
  }
  return Usages

# kwUsed, stReadingstReadingx2, endReadingx2,

# this is main function
# in: list ()

def createReading(consumptionMatrix,meterType):
  JSONreading = {}
  if (meterType == "Standard Electricity"):
    EnergyDescription = "Standard Electricity"
    meterType = 1
  for idx in consumptionMatrix:
      JSONreading.update(JSON_Usages(idx[0],idx[1],idx[2],idx[3],idx[4],EnergyDescription,meterType))

  return JSONreading



#############################
#############################
### MAIN
##############################


def main():

  XMLparser(inFile)

  return 0

if __name__ == '__main__':
  main()






