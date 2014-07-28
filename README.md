VBBRequest
==========

This little project lets you request train/bus data from BVG/VBB via python script. Therefor it uses an open interface provided by [hafas](http://www.hacon.de/hafas). 

vbbReq.py
---------
Script for communication with the hafas server. 

**Usage**<br>
Call this method to get a list object of connections, based on your parameters. <br>
`request(departure, destination, date, time, vehicle, direct, enableFoot):`<br>


**Parameters**<br>
* departure: String with station ID. You get a list with all station IDs in Berlin here: http://daten.berlin.de/kategorie/verkehr *(Download the current GTFS packed and look in stops.txt)*
* destination: Same as departure
* date: String like this: `'20140612'`
* time: String like this `'20:45'`
* vehicle: String like this `'0000000000000000'`. Every `0` represents a transport style. You can activate it by replacing it with a `1`. Example:`'0001000000000000'` means bus. (I couldn't find any documentation, telling me which `0` is which transportation style. So you have to find this out on your own)
* direct: Use `'1'` if you only want direct connections. If you also accept indirect connections, use `'0'` 
* enableFoot: `False` if you don't want to walk. Else `'True'`

**Return**<br>
You'll get a list object with the recieved data. If you want an example, just run `test():` or look [here](https://github.com/pascalweiss/vbbRequest/blob/master/example_request_vbbReq.txt)
  
**Requirements** <br>
* requests.py
* python2.7 *(I tested it only with 2.7.5, so I don't garantee, that it works with other versions)*


vbbStationInfo.py
-----------------
This is an example on how you can use vbbReq.py. It simulates a BVG scoreboard for the bus station Oberlandstr./Germaniastr.

**Pictures** <br>
<br>
![](http://www.upload-pictures.de/bild.php/57662,vbbreqscreenshotkopieJ55ZT.png) 

**TODO** <br>
*Just some suggestions*
* User input. At least for quitting the script. This should be one of the next steps (The curses modul is making your terminal look very messy after `ctrl + c`...)
* More Stations. Right now the script only asks for connections from Oberlandstr/Germaniastr. (This is a bus station in Berlin). Although you can request info for every station.
* Different transport styles. Right now, the script only asks for bus connections.
* VBB gives informations about accessibility. For example if a elevator is broken.

conReq.xml
----------
This is used by vbbReq.py as a template for it's posts to the hafas server. 


Links
-----
* Description by VBB: http://www.vbb.de/t_de/article/webservices/schnittstellen-fuer-webentwickler/5070.html
* Interface description by hafas: http://demo.hafas.de/xml/vbb/dai/hafasXMLInterface.xsd
* Example requests with http: http://images.vbb.de/assets/downloads/file/20930.zip (369.5 KB)

 

