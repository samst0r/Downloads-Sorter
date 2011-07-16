#!/usr/bin/python

import os
import time
import datetime
import shutil

class Sort:
	WEEK = datetime.timedelta(weeks=1)
	DAY = datetime.timedelta(days=1)
	YEAR = datetime.timedelta(days=30)

	def __init__(self):
		dirs = filter(os.path.isdir, os.listdir('.'))
			
		foundLastWeek = os.path.exists(os.getcwd() + '/Last Week')
		foundOlder = os.path.exists(os.getcwd() + '/Older')
		
		print '-------------------------'
		print '*    DOWNLOAD SORTER    *'
		print '*      by Sam Ward      *'
		print '-------------------------\n'
			
		if (not foundOlder):
			print 'Creating Older Directory...'
			os.mkdir(os.getcwd() + '/Older')
		if (not foundLastWeek):
			print 'Creating LastWeek Directory...'
			os.mkdir(os.getcwd() + '/Last Week')
		
		if (foundOlder and foundLastWeek):
			print 'Directories Already Exist...'
			
	def FileCreatedToday(self, file): 
		createdDay = datetime.datetime.fromtimestamp(os.path.getmtime(file))
		diff = createdDay > (datetime.datetime.now() - self.DAY) 
		
		if (diff):
			return True
		else:
			return False	
	def FileCreatedInLastSevenDays(self, file):
		createdDay = datetime.datetime.fromtimestamp(os.path.getmtime(file))
		diff = createdDay >= (datetime.datetime.now() - self.WEEK) 
		
		if (diff):
			return True
		else:
			return False
			
	def FileOlderThanWeek(self, file):
		createdDay = datetime.datetime.fromtimestamp(os.path.getmtime(file))
		
		diff = createdDay <= (datetime.datetime.now() - self.WEEK) 
		
		if (diff):
			return True
		else:
			return False
	
	# Move files into correct directories	
	def SortFiles(self):
		print 'Sorting Root Files...'
		# Don't include files that start with .(filename)
		for file in os.listdir(os.getcwd()):
			if (file[:1] != '.' and
				file != 'Last Week' and
				file != 'Older' and
				file != os.path.basename(__file__)):
			
			        if (self.FileCreatedToday(file)):
					print '  Leaving ' + file + ' in place.' 	
				elif (self.FileOlderThanWeek(file)):
					shutil.move(file, 'Older')
					print '  Moved ' + file + ' to Older.'
				elif (self.FileCreatedInLastSevenDays(file)):
					shutil.move(file, 'Last Week')
					print '  Moved ' + file + ' to Last Week.'
				
		print 'Sorting Last Week Folder...'
		lastWeekPath = os.path.join(os.getcwd(), 'Last Week')
		files = [f for f in os.listdir(lastWeekPath) if os.path.isfile( os.path.join(lastWeekPath, f)) or os.path.isdir( os.path.join(lastWeekPath, f))]
		for f in files:
			if (not self.FileCreatedInLastSevenDays(lastWeekPath + '/' + f)):
				shutil.move(os.getcwd() + '/Last Week/' + f, os.getcwd() + '/Older/')					
				print '  Moved ' + f + ' to Older.'
			else:
				print '  Leaving ' + f + ' in place.'					

def main():
	sorter = Sort()
	sorter.SortFiles()
	
if __name__ == "__main__":
	main()
