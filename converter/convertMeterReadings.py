#!/usr/bin/env python3
import os
import sys
import getopt

import time as t
import xml.etree.ElementTree as ET
import json


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
  combinedReadings = zip(consuption,readingDates[:-1],readingValues[:-1],readingDates[1:],readingValues[1:])
  #print readings[1][0]
  return combinedReadings
# kwUsed, dateStart, readingStart, dateEnd, readEnd,

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
    "EndReading": JSON_Reading(readingStart,DateEnd,meterType),
    "EnergyDescription":EnergyDescription
  }

  output = json.dumps(Usages) 
  #print (output)
  return output

# this is main function
# in: list ()
def createReading(consumptionMatrix,meterType):

  print consumptionMatrix
  if (meterType == "Standard Electricity"):
    EnergyDescription = "Standard Electricity"
    meterType = 1

  #Std info about meter
  Mpan = {"pc":217237189,
  "mtc":1575355055,
  "llfc":275683061,
  "distributorid":20463572,
  "uniqueid":695034916,
  "checkdigit":431389205,
  "state":2
  }
    
  Usages = ""    
  for idx in consumptionMatrix:
      print Usages
      Usages =  Usages + JSON_Usages(idx[0],idx[1],idx[2],idx[3],idx[4],EnergyDescription,meterType)

  EnergyUsage={
      "Start": 1,#consumptionMatrix[0][1],
      "End": 2,#consumptionMatrix[0][3],
      "Usages":Usages
  }

  ElectricMeter={
      'Mpan':Mpan,
      'EnergyUsage':EnergyUsage,
    'UniqueId' : "9e15f78c-14b7-4f01-81d4-80db67bb45db",
    "Type" : {
      "Description":"6 digit electricity meter",
      "DecimalPlaces":1,
      "Digits":6,
      "Units":0,
      "MaxReading":999999.9},
    'SerialNum' : "AV3RNX1JBVMI",
    'Latitude' : 51.4716939239492,
    'Longitude' : -2.59810170396113,
    'PostCode' : "BS6 7AR"
  }

  JSONreading = json.dumps(ElectricMeter)
  return JSONreading


#############################
#############################
### MAIN
##############################


def main():

  FFreadings = XMLparser(inFile)
  print "now JSON"
  JSON_output = createReading(FFreadings, "Standard Electricity")
  #print JSON_output

  # write file
  try:
    outFile = open("%s.JSON" % inFile[:inFile.index('.')], "w")
  except ValueError: #if file has no extension
    outFile = open("%s.JSON" % inFile, "w") 

  outFile.write(JSON_output)
  outFile.close()


  return 0

if __name__ == '__main__':
  main()






