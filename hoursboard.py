#!/usr/bin/python

# HoursBoard
# Copyright 2013 Nitesh Morajkar
# See LICENSE for details.

__author__ = 'Nitesh Morajkar'

import csv,time,sys,datetime,os,re

print """ _    _                        ____                      _ 
| |  | |                      |  _ \                    | |
| |__| | ___  _   _ _ __ ___  | |_) | ___   __ _ _ __ __| |
|  __  |/ _ \| | | | '__/ __| |  _ < / _ \ / _` | '__/ _` |
| |  | | (_) | |_| | |  \__ \ | |_) | (_) | (_| | | | (_| |
|_|  |_|\___/ \__,_|_|  |___/ |____/ \___/ \__,_|_|  \__,_|\n"""


now = datetime.datetime.now() # Get current timestamp


#{{ Prints Usage
def Usage():
	print "Usage: python " + sys.argv[0] + " " + now.strftime("%Y-%m-%d")
	sys.exit(0)
#}}

# Date argument
argDate = ''

if len(sys.argv) != 2:
	Usage()
else:
	argDate = sys.argv[1]

# {{ Open log file and parse csv
basePath = re.sub('/+', '/', open(os.path.dirname(os.path.realpath(__file__)) + '/conf', 'r').read().strip() + '/')

try:
	with open(basePath + argDate + '.log', 'rb') as csvfile:
		readObj = csv.reader(csvfile, delimiter=',', quotechar='|')
		data = {}
		i = 0
		for row in readObj:
			if row:
				if len(row) == 3:
					row2 = str(row[2])
				else:
					row2 = ''
				data[i] = {row[0]: [row[1], row2]}
				i=i+1
except IOError:
	print 'Screen Lock logs have not been found for ' + argDate + '. Seems, it was a holiday.'
	sys.exit(0)

# {{ Convert seconds to time format
def secToTime(sec):
    sec = int(sec)

    days = sec / 86400
    sec -= 86400*days

    hrs = sec / 3600
    sec -= 3600*hrs

    mins = sec / 60
    sec -= 60*mins
    return str(hrs) + " hrs " + str(mins) + ' min ' + str(sec) + ' sec'
# }}

# {{ Calculate Screen lock time and Screen unlock time
def parseLogs(data):
	# Calculate total time system was ON
	try:
		if now.strftime("%Y-%m-%d") != datetime.datetime.fromtimestamp(int(data[len(data)-1]['1'][0])).strftime('%Y-%m-%d'):
			totalTime = (int(data[len(data)-1]['1'][0]) - int(data[0]['1'][0]))
		else:
			totalTime = (int(time.time()) - int(data[0]['1'][0]))
	except KeyError:
		print "Seems you forgot to tag your logout."
		sys.exit(0)

	prev = ''
	i = 0
	logoutTagArray = []
	lockedTime = 0
	unlockedTime = 0
	for d in data:
		if i != 0:
			if i%2 == 0:
				try:
					if prev == '0':
						lockedTime = lockedTime + int(data[d]['1'][0]) - int(data[d-1]['0'][0])
						if data[d]['1'][1] != '':
							logoutTagArray.append([data[d]['1'][1], int(data[d]['1'][0]) - int(data[d-1]['0'][0])]);
					prev = '1'
				except IndexError:
					if prev == '1':
						unlockedTime = unlockedTime + int(data[d]['0'][0]) - int(data[d-1]['1'][0])
					prev = '0'
			else:
				try:
					if prev == '1':
						unlockedTime = unlockedTime + int(data[d]['0'][0]) - int(data[d-1]['1'][0])
					prev = '0'
				except IndexError:
					if prev == '0':
						lockedTime = lockedTime + int(data[d]['1'][0]) - int(data[d-1]['0'][0])
						if data[d]['1'][1] != '':
							logoutTagArray.append([data[d]['1'][1], int(data[d]['1'][0]) - int(data[d-1]['0'][0])])
					prev = '1'
		else:
			prev = '1'
		i=i+1

	unlockedTime = totalTime-lockedTime
	return {"time_list" : [totalTime, lockedTime, unlockedTime], "logout_tag": logoutTagArray}
# }}

# {{ Repeat provided string n times
def repeatString_N_times(str, length):
   return (str * ((length/len(str))+1))[:length]
# }}

# {{ Get max characters in first column
def getMaxWidth(table):
    """Get the maximum width of the given column index"""
    return max([len(row[0]) for row in table])
# }}

# {{ Display Tag report
def getTagReport(tagArray):
	columnwidth = getMaxWidth(tagArray)

	finalTagArray = []
	for item in tagArray:
		# item[0] - Tag name
		# item[1] - Time in seconds
		itemLen = len(item[0])
		if itemLen > columnwidth:
			diff = itemLen-columnwidth
		else:
			diff = columnwidth-itemLen
		finalTagArray.append(item[0] + repeatString_N_times(" ", diff) + "  " + str(secToTime(item[1])))
	return finalTagArray
# }} 


parsedData = parseLogs(data)

# {{ Print final stats
print "Total time:\t" + str(secToTime(parsedData['time_list'][0]))
print "Locked:\t\t" + str(secToTime(parsedData['time_list'][1]))
print "Unlocked:\t" + str(secToTime(parsedData['time_list'][2]))

if parsedData['logout_tag']:
	print "\nDetailed Tag Report\n"
	finalTagArray = getTagReport(parsedData['logout_tag'])
	for tagDetail in finalTagArray:
		print tagDetail

