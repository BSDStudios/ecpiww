ecpiww
======

This is code to connecting [EnergyCam](http://www.fastforward.ag/eng/index_eng.html) through HAN to IPFS. It got three parts:

* XML 2 JSON converter in python
* IPFS reader (not here yet)
* ecpiww in C, forked from FF repo


# XML 2 JSON converter

Energycam write data in the XML [ecpi log])(https://github.com/BSDStudios/electron-platform/wiki/Meter-Reading-API)
format. This script convert it to JSON, ready to be added to IPFS

* JSON format examples are on [IPFS](ipfs ls QmSaNYi5MmZ2GPza2XsP15aeiLmqvwvxxWJBxTB9yLNXm), generator code [is here](https://github.com/BSDStudios/electron-billing/blob/master/MeterReadingGenerator/EnergyCalculator.cs).
* Energycam write data (if you follow my wiki) in the XML [ecpi log])(https://github.com/BSDStudios/electron-platform/wiki/Meter-Reading-API) format.

## running code

```
python convertMeterReadings.py -l FF_ecpi_log.XML
```

This will output *ecpi_log.JSON file*

## status

At current stage code has:

* very minimal exception control - if file is wrong it will crash
* no check for consistency of the data (for ex time and result order)
	* it assumes readings are wrote in ascending order (as per normal FF setup)
* JSON output
	* data is outputted in descending order
	* in Jeremy code "Usages": have two field values, StartingTime and list of readings. I can't do it easly in python so for now it only output single field - list of readings

[ ] check dual Usage field with Jeremy

#ecpiww

This is code responsible for the working [EnergyCam RS](http://www.fastforward.ag/eng/index_eng.html) setup for Raspberry Pi, forked from FF repo.

## Checklist

[ ] debug problem with mW dongle
[ ] check if this is not due to [key number conversion](https://github.com/ffcrg/ecpiww/blob/master/linux/src/energycam/ecpiww.c#L613)
[ ] add few printf to wmbus.c to check connection with reader




Hardware needed to run this:
* Raspberry Pi
* FAST EnergyCam RF and FAST USB Communication Interface to configure the Energycam prior to installation
* AMBER Wireless M-Bus USB Adapter (http://amber-wireless.de/406-1-AMB8465-M.html)



Software:
  - dygraph (https://github.com/danvk/dygraphs)

Features:
 - The application shows you all received wireless M-Bus packages.
 - You can add meters that are watched. The received values of these are written into csv files and presented on the webserver.
 - The energy usage is shown as an interactive, zoomable chart of time on a website.
 - install.txt describes how to configure the raspberry and compile the sources


Trademarks

Raspberry Pi and the Raspberry Pi logo are registered trademarks of the Raspberry Pi Foundation (http://www.raspberrypi.org/)

