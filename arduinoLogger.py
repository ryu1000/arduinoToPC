#!/usr/bin/env python
# Intent: Connects to an Arduino operating as a data logger. Records data to an output file
# Author: Jose C. Campos
# Email: jccava09@gmail.com

print "\nPython Script loaded"
print "Starting program"
print "Importing libraries"
import serial
import time
import os
from datetime import datetime

# Constants
iterations=1
itergrid=[-1]
datagrid=[]
databit=0
readset=[]
firstRead=True

# Definitions
def debugmsg(message,stamp):
	with open(DEBUGOUT, "a") as db:
		db.write("\n %s" % message)
		db.write("\t %s" % stamp)

def write_readings(data):
	with open(DATAOUT, "w") as f:
		f.seek(0)
		f.write(data)

def is_number(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def readarduino(newdata):
	# Reads the data the arduino sent over serial
	# and is assuming it is in this format: 30.2,532.012,5 (CSV in other words)
	# it then searches for the commas and tries to break the data into an array
	iterations = newdata.count(',') # counts the number of commas to know how many datablocks are needed
	i=1 # Reset counter variable (it is reused elsewhere)
	itergrid=[-1] # Reset comma location array since this process is repeated for each data sample
	datagrid=[] # Reset the data array since this proccess is repeated for each data sample
	while i <= iterations: # Repeat the following for each comma found
		newcomma=newdata.find(',',itergrid[i-1]+1) # Identify the next comma using the array of located commas
		itergrid.append(newcomma) # Add this comma to the array of located commas
		databit=newdata[itergrid[i-1]+1:itergrid[i]] # The databit is the text between two commas ("... ,20, ..." = "20")
		if is_number(databit)==True: # Look at databit and determine if it could be a number using another definition
			databit=int(databit) # If databit could be a number, convert it into a number
		datagrid.append(databit) # Add the current data bit to the dataset
		i+=1 # Move on to the next comma
	databit=newdata[itergrid[i-1]+1:] # Make a databit for the text between the last comma and the end of line
	if is_number(databit)==True: # Repeat check to see if databit could be a number
		databit=int(databit) # If databit could be a number, convert it into a number
	datagrid.append(databit) # Add the current data bit to the dataset
	return datagrid # That should be the full array, so send it back to be saved

# Define names that may change
print "Setting file names"
DATAOUT='.txt' # This is the final CSV output after completion
DEBUGOUT='-debug.txt' # Where debug outputs go

# User setup variables
print "Getting user setup variables"
PORT = raw_input("Please enter COM port number (ex. /dev/ttyUSB0):")
DATAPREFIX = raw_input("Please enter data file prefix (without extension):")
DATAOUT=DATAPREFIX+DATAOUT
DEBUGOUT=DATAPREFIX+DEBUGOUT

# Initializing Arduino Communication
print "Starting serial port communications"
ser = serial.Serial(PORT, 9600)
debugmsg("Serial Port Started",datetime.now())
while 1:
	if firstRead == True:
		firstRead = False
		print "Dropping first reading"
		currentread=ser.readline()
		time.sleep(2)
	else:
		# Get new data
		currentread=ser.readline()
		debugmsg(currentread,datetime.now())
		write_readings(currentread)
		# Convert data to array
		readset=readarduino(currentread)
		print readset

