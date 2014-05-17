vbbRequest
==========

This little project lets you request train/bus data from BVG/VBB via python script. Therefor it uses an open interface provided by [hafas](http://www.hacon.de/hafas). 

vbbReq.py
---------
Script for communication with the hafas server. 

**Usage**
`request(departure, destination, date, time, vehicle, direct, enableFoot):`
Call this method to get a list object of connections, based on your parameters.

*Parameters*
* departure: String with station ID. You get a list with all station IDs in Berlin here: http://daten.berlin.de/kategorie/verkehr *(Download the current GTFS packed and look in stops.txt)*
* destination: Same as departure
* date: String like this: `'20140612'`
* time: String like this `'20:45'`
* vehicle: String like this `'0000000000000000'`. Every `0` represents a transport style. You can activate it by replacing it with a `1`. Example:`'0001000000000000'` means bus. (I couldn't find any documentation, telling me which `0` is which transportation style. So you have to find this out on your own)
* direct: Use `'1'` if you only want direct connections. If you also accept indirect connections, use `'0'` 
* enableFoot: `False` if you don't want to walk. Else `'True'`

*Return*
You'll get a list object with the recieved data. If you want an example, just run `test():` or look here 
  

**Requirements**
* requests.py


vbbStationInfo.py
-----------------
This is an example on how you can use vbbReq.py. It simulates a BVG scoreboard for the bus station Oberlandstr./Germaniastr. 
**Pictures** 
TODO

**TODO**
There could be an input field, where the user can enter the name for his desired station. 

conReq.xml
----------
To requesting data, you need to post an .xml to the hafas interface. canReq.xml is the template for vbbReq.py.

Links
-----
* [VBB description](http://www.vbb.de/t_de/article/webservices/schnittstellen-fuer-webentwickler/5070.html)
* [Interface description by hafas](http://demo.hafas.de/xml/vbb/dai/hafasXMLInterface.xsd)
* [Example requests with http (zip file 369.5 KB)](http://images.vbb.de/assets/downloads/file/20930.zip)
* You need to []
* 

