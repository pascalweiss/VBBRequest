import time 
from operator import itemgetter
from subprocess import call
import os
import re
import curses
from _thread import start_new_thread
from bvggrabber.api.actualdeparture import ActualDepartureQueryApi
from wetter24grabber.api.queryapi import WetterQueryApi

 


#import pywunderground 

screen = curses.initscr() 
curses.start_color()
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



# To alter the request procedure, it must be ensured, that 
# The new approach yields a list of dictionaries, where each 
# dict represents one connection. 
# Each connection has a key for 'vehicle', for 'direction' and for 'depTime'
def printConnectionList(departures):
    screen.clear()
    terminalSize = os.popen('stty size', 'r').read().split()
    terminalWidth = int(terminalSize[1])
    terminalHeight = int(terminalSize[0])
    string = ''
    row = 1
    column = 0
    for dep in departures:
        if row < terminalHeight-3:
            row += 1
            screen.addstr(row, 1, re.sub('Bus ', '', dep.line))
            screen.addstr(row, 12, dep.end)
            screen.addstr(row, terminalWidth-8, dep.when.strftime("%H:%M"))
            screen.refresh()

def oberlandstrReqeust():
    departures = None
    try:
        a = ActualDepartureQueryApi("Oberlandstr./Germaniastr. (Berlin)").call()
        departures = a.departures[0][1]
    except: 
        None
    else: 
        None
    return departures
    

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

def temperaturePrint(something):
    response = None
    temp_txt = ""
    rain_prob_txt = ""
    sunshine_length_txt = ""
    
    api = WetterQueryApi("12099", "16156188")
    try:
        response = api.call()
        temp_txt = response.temp + "C"
        rain_prob_txt = response.rain + "mm"
        sunshine_length_txt = response.sun + "h"
        wind_txt = response.wind + "km/h"

    except:
        None
    else:
        None 
    weather_txt = "sun: " + sunshine_length_txt + "  rain: " + rain_prob_txt + "  temp: " + temp_txt + "  wind: " + wind_txt
    terminalSize = os.popen('stty size', 'r').read().split()
    terminalHeight = int(terminalSize[0])  
    terminalWidth = int(terminalSize[1]) 
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    screen.addstr(terminalHeight-1,terminalWidth-len(weather_txt)-1,weather_txt, curses.color_pair(1))
    if type(something) == 'str':
        screen.addstr(terminalHeight-1,0, something)
    else:
        screen.addstr(terminalHeight-1,0,str(something))
    screen.refresh()

def nextRequestTime(departures, lastTime):
    nextTime = departures[0].when.strftime("%H:%M") + ':59'
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
        nextHour = '0'+ nextHour
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

def keyboardInput():
    while True:
        os.system("afplay /System/Library/Sounds/Funk.aiff")
        input = raw_input()
        if input == "q":
            exit()

def displayThread():
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
        currentSecond = int(currentTime[6:])
        currentDate = getCurrentDate()
        printCurrentTimeAndDate()
        if currentTime == nextReqTime or firstRequest == True or (currentMinute % 15 == 0 and currentSecond == 59):
            firstRequest = False
            number += 1
            printRequestNumber("Connecting...")
            departures = oberlandstrReqeust()
            if departures:
                printConnectionList(departures)
                nextReqTime = nextRequestTime(departures, nextReqTime)
                x=1
            else:
                nextReqTime = requestIn5Min()
            printRequestNumber(number)
            debugString = 'next request: '+nextReqTime
            temperaturePrint(debugString)
        time.sleep(0.5)

if __name__ == '__main__':
    start_new_thread(displayThread, ())
    while True:
        x = screen.getch()
        if x == 113:
            curses.nocbreak()
            screen.keypad(0)
            curses.echo()
            curses.endwin()
            exit()
