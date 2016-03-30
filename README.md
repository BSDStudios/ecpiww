ecpiww
======

This is an update to [EnergyCam](http://www.fastforward.ag/eng/index_eng.html) setup for Raspberry Pi, created by FF


Checklist

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

