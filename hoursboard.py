#!/usr/bin/python

# HoursBoard
# Copyright 2013 Nitesh Morajkar
# See LICENSE for details.

__author__ = 'Nitesh Morajkar'

import csv,time,sys,datetime

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
basePath = open('conf', 'r').read()
try:
	with open(basePath + argDate + '.log', 'rb') as csvfile:
		readObj = csv.reader(csvfile, delimiter=',', quotechar='|')
		data = {}
		i = 0
		for row in readObj:
			if row:
				data[i] = {row[0]: row[1]}
				i=i+1
except IOError:
	print 'Screen Lock logs have not been found for ' + argDate + '. Seems, it was a holiday.'
	sys.exit(0)

unlockedtime = 0
lockedtime = 0;

i = 0

# {{  Calculate total time system was ON
if now.strftime("%Y-%m-%d") != datetime.datetime.fromtimestamp(int(data[len(data)-1]['1'])).strftime('%Y-%m-%d'):
	totalTime = (int(data[len(data)-1]['1']) - int(data[0]['1']))
else:
	totalTime = (int(time.time()) - int(data[0]['1']))


# {{ Convert seconds to time format
def sec_to_time(sec):
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
prev = ''
for d in data:
	if i != 0:
		if i%2 == 0:
			try:
				if prev == '0':
					lockedtime = lockedtime + int(data[d]['1']) - int(data[d-1]['0'])
				prev = '1'
			except IndexError:
				if prev == '1':
					unlockedtime = unlockedtime + int(data[d]['0']) - int(data[d-1]['1'])
				prev = '0'
		else:
			try:
				if prev == '1':
					unlockedtime = unlockedtime + int(data[d]['0']) - int(data[d-1]['1'])
				prev = '0'
			except IndexError:
				if prev == '0':
					lockedtime = lockedtime + int(data[d]['1']) - int(data[d-1]['0'])
				prev = '1'
	else:
		prev = '1'
	i=i+1

lockedTime = lockedtime
unlockedTime = totalTime-lockedTime

# {{ Print final stats
print "Total time:\t" + str(sec_to_time(totalTime))
print "Locked:\t\t" + str(sec_to_time(lockedTime))
print "Unlocked:\t" + str(sec_to_time(unlockedTime))

