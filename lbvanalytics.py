import pandas as pd
import re

# Checks if the line starts with a date in the form of "[01-05-2018 14:30:25]"
def startsWithDate(s):
	pattern = '^(|.)\[(\d\d-\d\d-\d\d\d\d) (\d\d:\d\d:\d\d)\]'
	result = re.match(pattern, s)

	if result:
			return True
	return False

# Checks if the message (exluding the date and time) starts with an author
def startsWithAuthor(s):
	patterns = [
			'([\w]+):',                        					# First Name
			'([\w]+[\s]+[\w]+):',              					# First Name + Last Name
			'([\w]+[\s]+[\w]+[\s]+[\w]+):',    					# First Name + Middle Name + Last Name
			'([\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+):',   # First Name + Middle Name + Middle Name + Last Name
			'([+]\d{2} \d{5} \d{5}):',         					# Mobile Number (India)
			'([+]\d{2} \d{3} \d{3} \d{4}):',  					# Mobile Number (US)
			'([+]\d{2} \d{4} \d{7})'           					# Mobile Number (Europe)
	]
	pattern = '^' + '|'.join(patterns)
	result = re.match(pattern, s)

	if result:
			return True
	return False

# Get the date, time, author and message data from a line
def getDataPoints(s):
	splitted = s.split(']') 						
	dateTime = splitted[0].replace('[', '') 
	date, time = dateTime.split(' ')		
	message = splitted[1].strip()					

	# Checks if the message starts with an author, otherwise the author will be None
	if startsWithAuthor(message):
		splitMessage = message.split(': ')		
		author = splitMessage[0]
		message = ' '.join(splitMessage[1:])
	else:
		author = None

	return date, time, author, message

# Parse the data of the .txt file of the specified path
def parseData(path):

	# This will be the raw parsed data, that you can use for example for a pandas data frame
	parsedData = []

	with open(path, "r", encoding="utf-8") as f:
		
		# Save message in the buffer for multiline messages to save as one data entry
		messagebuffer = []
		date, time, author = None, None, None

		while True:
			line = f.readline()
			if not line:
				# Otherwise you miss the final message in the data
				if len(messagebuffer) > 0:
					parsedData.append([date, time, author, ' '.join(messagebuffer)])
				break

			line = line.strip()

			# Handles multiline messages
			if(startsWithDate(line)):
				if(len(messagebuffer) > 0):
					parsedData.append([date, time, author, ' '.join(messagebuffer)])
				messagebuffer.clear()
				date, time, author, message = getDataPoints(line)
				messagebuffer.append(message)
			else:
				messagebuffer.append(line)
	
	return parsedData

# Specify here the path of your .txt file
filepath = "lbvdata.txt"
parsedData = parseData(filepath)

# Now do fun stuff










		
