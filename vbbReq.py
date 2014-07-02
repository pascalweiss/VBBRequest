#! /usr/bin/python2.7
# _*_ coding: latin-1 _*_ 
#TODO brauch ich das???
import requests
import xml.dom.minidom as dom
import codecs
import os

# It's possible that a train won't stop at the station, therefor vbb uses the
# 'getIn' Attribute at the <Dep> Element. This attribute is ignored in this
# version. So the train might not stop, even thou this script says so... You
# can add this, if you want ;) 

def test ():
    bus = '0001000000000000'
    # If the example doesn't work, you might need to update the date-parameter in the
    # next line.
    postDict = newPostDict('9068205', '9017101', '20140702', '12:00', bus, '0')
    postXML = newPostXML(postDict)
    requestXML = requestDataFromVBB(postXML)
    if requestXML is not None:
        connectionsList = getConnectionsList(requestXML, False)
        printConnectionsList(connectionsList)
    #requestXML.close()

def request(departure, destination, date, time, vehicle, direct, enableFoot):
    postDict = newPostDict(departure, destination, date, time, vehicle, direct)
    postXML = newPostXML(postDict)
    requestXML = requestDataFromVBB(postXML)
    if requestXML is not None:
        connectionsList = getConnectionsList(requestXML, enableFoot)
        #requestXML.close()
        return connectionsList


def getConnectionsList(requestXML, enableFoot):
    tree = dom.parseString(requestXML)
    #tree = dom.parse('output.xml')
    connectionsList = []
    for connection in tree.getElementsByTagName('Connection'):
        if not (connection.parentNode.getAttribute('type') == 'IV' and enableFoot == False):
            auxiliary = 1
            conList = []
            for conSection in connection.getElementsByTagName('ConSection'):
                conSectDict = {'depStation':'','depTime':'','vehicle':'','direction':'','arrStation':'','arrTime':''}
                for departure in conSection.getElementsByTagName('Departure'):
                    for depStation in departure.getElementsByTagName('Station'):
                        conSectDict['depStation'] = depStation.getAttribute('name').encode('utf-8')
                    for depTime in departure.getElementsByTagName('Time'):
                        departureTime =  depTime.firstChild.data.strip().encode('utf-8')
                        departureTime = departureTime[3:]
                        conSectDict['depTime'] = departureTime.encode('utf-8')
                for arrival in conSection.getElementsByTagName('Arrival'):
                    for arrStation in arrival.getElementsByTagName('Station'):
                        conSectDict['arrStation'] = arrStation.getAttribute('name').encode('utf-8')
                    for arrTime in conSection.getElementsByTagName('Time'):
                        conSectDict['arrTime'] = arrTime.firstChild.data.strip().encode('utf-8')
                for journey in conSection.getElementsByTagName('Journey'):
                    for attribute in journey.getElementsByTagName('Attribute'):
                        if attribute.getAttribute('type') == 'NAME':
                            for text in attribute.getElementsByTagName('Text'):
                                conSectDict['vehicle']= text.firstChild.data.strip().encode('utf-8')
                        elif attribute.getAttribute('type') == 'DIRECTION':
                            for text in attribute.getElementsByTagName('Text'):
                                conSectDict['direction'] = text.firstChild.data.strip().encode('utf-8')
                if auxiliary == 1:
                    conList.append(departureTime)
                    auxiliary = 0
                conList.append(conSectDict)
        connectionsList.append(conList)
    return connectionsList



        # Use def NewPostDict(...) as parameter
def newPostXML(postDict):
    postXML = os.path.join(os.path.dirname(__file__), 'conReq.xml')
    tree = dom.parse(postXML)
    for conReq in tree.firstChild.childNodes:
        if conReq.nodeName == 'ConReq':
            for node1 in conReq.childNodes:
                if node1.nodeName == 'Start':
                    for node2 in node1.childNodes:
                        if node2.nodeName == 'Station':
                            node2.setAttribute('externalId', postDict['startStation'])
                        elif node2.nodeName == 'Prod':
                            node2.setAttribute('prod', postDict['vehicle'])
                            node2.setAttribute('direct', postDict['direct'])
                elif node1.nodeName == 'Dest':
                    for node2 in node1.childNodes:
                        if node2.nodeName == 'Station':
                            node2.setAttribute('externalId', postDict['destStation'])
                elif node1.nodeName == 'ReqT':
                    node1.setAttribute('date', postDict['date'])
                    node1.setAttribute('time', postDict['time'])
    return tree.toxml()


# Give the dictionary only strings.
# startStation: Look in ./open_vbb_data/stops.txt...
# date:         For Example '20140516' for 16.05.2014
# time:         for Example '12:45'
# vehicle:      For Example '0001000000000000'. This means "bus".
#               Set the other '0' to '1', if you wan't to enable
#               other vehicles
# direct:       If you wan't a direct connection, set this to '1'.
#               Otherwise set this to '0
def newPostDict(startStation, destStation, date, time, vehicle, direct):
    return {'startStation': startStation, 'destStation': destStation, 'date': date, 'time': time, 'vehicle': vehicle, 'direct': direct}

# Use def newPostXML(...) as parameter
def requestDataFromVBB(postXML):
    URL = "http://demo.hafas.de/bin/pub/vbb-fahrinfo/relaunch2011/extxml.exe/"
    x = 0
    while x != 3:
        try:
            request = requests.post(URL, data=postXML).text
            return request.encode('latin-1')
            break;
        except:
            x += 1

def printConnectionDict(conDict):
    print conDict
    string = ''
    string += conDict['depStation']+' '
    string += conDict['depTime']+' '
    string += conDict['arrStation']+' '
    string += conDict['arrTime']+' '
    string += conDict['vehicle']+' '
    string += conDict['direction']
    print string

def printConnectionsList(connectionsList):
    print connectionsList
    line = ''
    number = 1
    for connection in connectionsList:
        for conDict in connection:
            if type(conDict) == 'dict':
                printConnectionDict(conDict)
    print line
    

# Uncomment to test this
#test()
