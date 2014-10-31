'''
Graph Theory : Exploratory Analysis of Tweets
Author: Syed Muhammad Ali
Version 0.1: May 6, 2014
Version 0.2: May 26, 2014

Note: Make sure you've replace \r\n\r\n\r\n with \r\n---end--- in data files.
'''

import json
import networkx as nx
import matplotlib.pyplot as plt
from sets import Set
from os import listdir;
from networkx.readwrite import json_graph
from nugt14 import Tweet

### Read dataset from files for preprocessing ###
filenames = listdir("./data/");

dataset = [];
for fn in filenames:
	print "Processing ", fn
	fin = open("data/"+fn, "r");

	while True:
		line = fin.readline();
		
		if not line:
			break;
		
		line.rstrip();
		account, tweet_id = line.split(" ");
		tweet_id = int(tweet_id.rstrip());
		
		line = fin.readline().rstrip();
		date_str = line[6:];
		
		line = fin.readline().rstrip(); #line is either reply-to or the tweet
		
		reply_to = "";
		if(line[0:11] == "In-Reply-To"): #if reply too
			reply_to = line[13:];
			line = fin.readline().rstrip(); #then make it point to tweet line
		
		tmp = "";
		tweet = "";
		while tmp.rstrip() != "---end---":
			tweet += tmp;
			tmp = fin.readline();
		tweet.lstrip().rstrip();
		
		t = Tweet(account, tweet_id, date_str, reply_to, ''.join([i if ord(i) < 128 else ' ' for i in tweet]));
		dataset.append(t);
		
	fin.close();

### Print VIS array for Nodes and Edges ###
# node_id = 1; #unique node index
people = Set();
hashes = Set();

nodeIndex = dict();
freqmap = dict(); #captures how many times an entitiy has been refered to

nodes = [];
edges = [];

for d in dataset: #identify people and hashtags
	persontags = d.extractTags();
	hashtags = d.extractHashtags();
	
	if "@"+d.account not in people:
		# print "ADDING: @", d.account
		people.add("@"+d.account);
		freqmap["@"+d.account] = 1;
	
	for p in persontags:
		if p not in freqmap:
			freqmap[p] = 1;
		else:
			freqmap[p] += 1;
			
		people.add(p);
	
	for h in hashtags:
		if h not in freqmap:
			freqmap[h] = 1;
		else:
			freqmap[h] += 1;
			
		hashes.add(h);


G = nx.Graph();
#Draw people and hashtags with unique Ids
#This adds people who were retweeted by seed - but were not directly involved
for p in people:
	# nodeIndex[p] = node_id;
	# node_id += 1;
	
	G.add_node(p);
	#nodes.append(Node(nodeIndex[p], freqmap[p], p, p));
	
for h in hashes:
	# nodeIndex[h] = node_id;
	# node_id += 1;
	
	G.add_node(h);
	#nodes.append(Node(nodeIndex[h], freqmap[h], h, h, "square"));

#for each Tweet
for d in dataset:
	persontags = d.extractTags();
	hashtags = d.extractHashtags();
	
	#nodeIndex[d.tweet_id] = node_id; node_id += 1;
	#nodes.append(Node(d.tweet_id, 1, "Tweet", "Tweet by " + d.account + " on " + d.date_str));
	
	#This loop makes account holder's network
	for p in persontags:
		G.add_edge("@"+d.account, p);
		# edges.append(Edge(nodeIndex[p], d.tweet_id, 1, "associated with"));
	
	for h in hashtags:
		G.add_edge("@"+d.account, h);
		#G.add_edges_from( zip(persontags, [h]*len(persontags)) ); #add edge from each person related to that hashtag
		#edges.append(Edge(d.tweet_id, nodeIndex[h], 1, "is about"));
	
	#edges.append(Edge(nodeIndex["@"+d.account], d.tweet_id, 1, "tweeted"));

print "People: ", len(people), " Avg: ", len(people)/len(filenames), " Hashes: ", len(hashes);
print "Connected Components (Originally): ", len(nx.connected_components(G));

# code to check cc after delete
for fn in filenames:
	account = "@"+fn[:-4];
	
	tmp_graph = G.copy();
	tmp_graph.remove_node(account);
	
	print "Connect Components w/o ", account, ": ", len(nx.connected_components(G));