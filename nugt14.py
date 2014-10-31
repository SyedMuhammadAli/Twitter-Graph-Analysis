import re

class Node:
	def __init__(self, id, value, label, title, shape = "ellipse"):
		self.id = id;
		self.value = value;
		self.label = label;
		self.title = title;
		self.shape = shape;
	
	def toJSON(self):
		return json.dumps(self.__dict__);

class Edge:
	def __init__(self, src, dest, value, title):
		self.src = src;
		self.to = dest;
		self.value = value;
		self.title = title;
	
	def toJSON(self):
		return json.dumps(self.__dict__).replace("\"src\"", "\"from\"");

class Tweet:
	def __init__(self, account, tweet_id, date_str, reply_to, tweet):
		self.account = account;
		self.tweet_id = int(tweet_id);
		self.date_str = date_str;
		self.reply_to = reply_to;
		self.tweet = tweet;
		self.regex = "[^ #@\",\n\./:!')]+"
	
	def printAsString(self):
		print self.account, self.tweet_id, self.date_str, self.reply_to, self.tweet;
		
	def extractTags(self):
		return re.findall("@"+self.regex, self.tweet);
	
	def extractHashtags(self):
		return [h.lower() for h in re.findall("#"+self.regex, self.tweet)];
		
################################################
#Function Defnitions
# Utiliy functions to faciliate graph analysis
################################################

#foo