#! /usr/bin/python2.7
# _*_ coding: utf-8 _*_
import vbbReq
import time 
from operator import itemgetter
from subprocess import call
import os
import curses
#import pywunderground 

screen = curses.initscr() 
curses.noecho() 
curses.curs_set(0) 
screen.keypad(1) 


def cursesSettings():
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)

__name__='__main__'

def sortConnectionList(connectionList):
    newList = []
    afterMidnightList = []
    highestHour = 0
    for direction in connectionList:
        for connection in direction:
            time = connection[0]
            if highestHour < time[:2]:
                highestHour = time[:2]
            if time[:2] < '12':
	    #if time[:2] == '00' or time[:2] == '01' or time[:2] == '02' or time[:2] == '03' or time[:2] == '04' or time[:2] == '05':
                afterMidnightList.append(connection)
            else:
                newList.append(connection)
    if int(highestHour) > 22:
        afterMidnightList = sorted(afterMidnightList, key=itemgetter(0))
        newList = sorted(newList, key=itemgetter(0))
        result = newList + afterMidnightList
        return result
    else:
        result = sorted((afterMidnightList + newList), key=itemgetter(0))
        return result



def printConnectionList(connectionList):
    screen.clear()
    terminalSize = os.popen('stty size', 'r').read().split()
    terminalWidth = int(terminalSize[1])
    terminalHeight = int(terminalSize[0])
    string = ''
    row = 1
    column = 0
    for connection in connectionList:
        if row < terminalHeight-3:
            row += 1
            dict = connection[1]
            screen.addstr(row, 1, dict['vehicle'])
            screen.addstr(row, 12, dict['direction'])
            screen.addstr(row, terminalWidth-8, dict['depTime'])
            screen.refresh()

def oberlandstrReqeust(time, date):
    list =[]
    bus = '0001000000000000'
    komturstr = vbbReq.request('9068205', '9069203', date, time, bus, '1',False)
    hermannstr = vbbReq.request('9068205','9079221', date, time, bus, '1',False)
    mehringdamm = vbbReq.request('9068205','9017101', date, time, bus, '0',False)
    #altTempelhof = vbbReq.request('9068205','9068202', date, time, bus, '1')
    if komturstr is not None:
        list.append(komturstr)
    if mehringdamm is not None:
        list.append(mehringdamm)
#list.append(altTempelhof)
    if hermannstr is not None:
        list.append(hermannstr)
    list = sortConnectionList(list)
    return list

def getCurrentDate():
    return time.strftime('%d:%m:%Y')

def getCurrentTime ():
    ttime = time.localtime()
    hours = ''
    minutes = ''
    seconds = ''
    if len(str(ttime[3])) == 1:
        hours = '0' + str(ttime[3])
    else:
        hours = str(ttime[3])
    if len(str(ttime[4])) == 1:
        minutes = '0' + str(ttime[4])
    else:
        minutes = str(ttime[4])
    if len(str(ttime[5])) == 1:
        seconds = '0' + str(ttime[5])
    else:
        seconds = str(ttime[5])

    return hours + ':' + minutes + ':' + seconds


def getCurrentDateForRequest():
    return time.strftime('%Y%m%d')

def getCurrentTimeForRequest ():
    ttime = time.localtime()
    hours = ''
    minutes = ''
    if len(str(ttime[3])) == 1:
        hours = '0' + str(ttime[3])
    else:
        hours = str(ttime[3])
    if len(str(ttime[4])) == 1:
        minutes = '0' + str(ttime[4])
    else:
        minutes = str(ttime[4])

    return hours + ':' + minutes

def printCurrentTimeAndDate():
    currentTime = getCurrentTime()
    currentDate = getCurrentDate()
    screen.addstr(0,0,currentTime + '  ' + currentDate)
    screen.refresh()

def debugPrint(something):
    terminalSize = os.popen('stty size', 'r').read().split()
    terminalHeight = int(terminalSize[0])  
    terminalWidth = int(terminalSize[1]) 
    hackText = 'Hacking BVG since 16.05.2014'
    screen.addstr(terminalHeight-1,terminalWidth-len(hackText)-1,hackText)
    if type(something) == 'str':
	screen.addstr(terminalHeight-1,0, something)
    else:
        screen.addstr(terminalHeight-1,0,str(something))
    screen.refresh()

def nextRequestTime(request, lastTime):
    con = request[0]
    nextTime = con[0][:5] + ':59'
    nextHour = int(nextTime[:2])
    nextMinute = int(nextTime[3:][:2])
    if nextTime == lastTime:
        nextMinute += 1
        if nextMinute > 59:
            nextMinute = nextMinute - 60
            nextHour += 1
            if nextHour > 23:
                nextHour = nextHour - 24
    nextMinute = str(nextMinute)
    nextHour = str(nextHour)
    if len(nextMinute) < 2:
        nextMinute = '0' + nextMinute
    if len(nextHour) < 2:
        nextHour = '0'+nextHour
    nextTime = nextHour + ':' + nextMinute + ':59' 
    return nextTime

def requestIn5Min():
    nextTime = getCurrentTime()
    nextHour = int(nextTime[:2])
    nextMinute = int(nextTime[3:][:2])
    nextMinute += 5
    if nextMinute >= 60:
        nextMinute -= 60
        nextHour += 1
        if nextHour > 23:
            nextHour -= 24
    nextMinute = str(nextMinute)
    nextHour = str(nextHour)
    if len(nextMinute) < 2:
        nextMinute = '0' + nextMinute
    if len(nextHour) < 2:
        nextHour = '0'+nextHour
    nextTime = nextHour + ':' + nextMinute + ':59' 
    return nextTime
    

def printRequestNumber(number):
    terminalSize = os.popen('stty size', 'r').read().split()
    terminalWidth = int(terminalSize[1])
    terminalHeight = int(terminalSize[0])
    screen.addstr(0,terminalWidth-10-len(str(number)), 'Requests: ' + str(number))
    screen.refresh()

if __name__ == '__main__':
    cursesSettings()
    input = ''
    nextReqTime = '23:23:23'
    currentDate = ''
    currentTime = ''
    firstRequest = True
    number = 0
    while True: 
        currentTimeForRequest = getCurrentTimeForRequest()
        currentDateForRequest = getCurrentDateForRequest()
        currentTime = getCurrentTime()
        currentMinute = int(currentTime[3:][:2])
        currentDate = getCurrentDate()
        printCurrentTimeAndDate()
        debugString = 'next request: '+nextReqTime
        debugPrint(debugString)
        if currentTime == nextReqTime or firstRequest == True or currentMinute % 15 == 0:
            firstRequest = False
            number += 1
            request = oberlandstrReqeust(currentTimeForRequest, currentDateForRequest)
            if request:
                printConnectionList(request)
                nextReqTime = nextRequestTime(request, nextReqTime)
            else:
                nextReqTime = requestIn5Min()
            printRequestNumber(number)
        time.sleep(0.5)
    curses.endwin()
