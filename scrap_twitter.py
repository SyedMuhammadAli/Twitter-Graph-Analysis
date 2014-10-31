import os
import sys
import subprocess

def retrieveTweets(account, fh):
	proc = subprocess.Popen(['twitter-log', account], stdout=fh);
	print "Processing tweets from @",account; 
	proc.wait();
	fh.flush();

def scrapAccounts(accounts_list):
	for i in range(1, len(accounts_list)):
		fileName = "data/"+accounts_list[i]+".txt";
		doPrepend = False;
		
		if os.path.isfile(fileName):
			print "File already exist. Stacking tweets...";
			fileName += ".tmp"
			doPrepend = True;
			
		fh = open(fileName, "w");
		retrieveTweets(accounts_list[i], fh);
		fh.close();
		
		#because three new lines is not a reliable seperator
		fh = open(fileName, "r+");
		formattedContent = fh.read().replace("\n\n\n", "\n---end---");
		fh.seek(0);
		fh.truncate();
		fh.write(formattedContent);
		fh.close();
		
		#merge files
		buff = ""; #free memory
		if doPrepend:
			fh_new = open(fileName, "r");
			fh_old = open(fileName[:-4], "r+");
			
			fh_old_firstline = fh_old.readline();
			
			for line in fh_new:
				if line == fh_old_firstline:
					buff += line;
					break;
				else:
					buff += line;
			
			buff += fh_old.read();
			fh_old.seek(0);
			fh_old.truncate();
			fh_old.write(buff);
			
			fh_new.close();
			fh_old.close();
			os.remove(fileName);
	
if len(sys.argv) < 2:
	sys.exit('You need to pass twitter account name as command line arguments\nUsage: scrap_twitter.py accountName1 accountName2 ... accountName N');

scrapAccounts(sys.argv);