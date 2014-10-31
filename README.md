***
Twitter-Graph-Analysis
======================
***

This information presented hereafter is copied from the project report's first draft. It may, or may not be fully correct.

The intent of this readme file is to provide an introduction to the project only. 

Tools:

We used python for the development of the tool. In specific, we used NetworkX [4], and Metaplot [5] for internal representation and drawing of graph. We used Metaplot for plotting graphs drawn with NetworkX. We used Gephi [7] for drawing the actual graph, using the Pajek format for representing the graph. We used Pajek [8] format due to its apparent simplicity with representing graph. 

Data Gathering:

We have developed a wrapper script that uses twitter-log [3] to extract tweets from twitter account. The main advantage of using this tool is that is bypasses twitters’ restriction of 200 tweets per request with using Twitter API. Dataset of 98k tweets of 37 political accounts. The topology of our graph is described as follows.

•	A seed twitter account is a node.

•	A hashtag is a node.

•	Every person tagged inside a tweet is a node.

•	People tagged are connected to the tagger.

•	Account is connection to hashtags they mentioned.

Data Extraction:

After the data was extracted using scrap\_twitter.py we used gt.py to extract, transform, and load the data into Tweet, Node, and Edge classes that we created to effectively manage data for further processing. The format of the data extracted by scrap\_twitter.py was as follows:

•	First line is account name followed by tweet id.

•	Second line is date followed a date time string

•	Third line as an optional reply-to, in case the tweet was a reply to some other tweet.

•	The fourth line the tweet message followed by thee blank lines (these are replaced by ---end--- using Notepad++).


We ignored all characters that were not in the utf-8 format, to simplify string handling. Further, we do not use the tweet content as of yet. We extracted the tagged people, and hashtags using regular expressions which can be found inside the Tweet class in gt.py.

The tool beings by reading all the tweets into a Tweet object. The Tweet class helps manipulate the data inside the tweet effectively while keeping room for future improvements (like date string processing). The two key methods in this class are extractTaggedPeople, and extractHashtags. They used simple regular expression which are basically say that anything followed by a # or @ that is not a space character is a string of interest. Obviously, our regex is a little more complicated that, but the general notion is the same as stated earlier.

After the first round of extraction, we have everything in a list of tweets. We then iterate over all tweets and identify unique people, and hashtags in the entire dataset. We do this by adding them to the python’s Set object, which does this automatically, because it’s a set.

Next we add the tweet’s data into the NetworkX [4] graph object as per the topology we described earlier. We used the Node and Edge class to store further complex relations, but commented them our after we adopted NetworkX [4]. They can still be of use when visualizing millions of tweets, because they enable extension for complex analysis, and serialization to disk. 
 
The key challenge in this project was to plot such a massive graph. With over a hundred thousand nodes and edges. We first attempted to draw the graph using vis.js [6] (a popular javascript canvas based library), but failed because of its ability to draw large graphs. Vis.js takes over 5 minutes to draw even a simple graph with over 200 nodes. It is, however, good to visualize small networks and graphs.

Analysis (of results):

We plotted 97,739 tweets from 37 different policial accounts. The resulting graph was a single connected component which shows how interconnected the social media network is. Using Gephi we identified that less that 20% of the nodes span the entire network (as connected neighbors light up).
In total, 37 politicians interacted with 18,878 people by directly engaging then in conversations or retweeting them. That’s an average of 510 per politician in the timespan of the publically available tweets. They talked on 6,017 topics (hashtags).
We structured the graph such that if a someone mentioned other accounts in their tweet, they tagged people are connected to the tagger by an edge. Also, the person who tweeted is connected to all the hashtags they used. For our analysis, as suggested, we checked if removing a politician disconnects the graph or not. For this, we iterated over all account names, and deleted them one by one and check the resulting number of connected components. 

REFERENCES
[1]	G. O. Young, “Synthetic structure of industrial plastics (Book style with paper title and editor),” 	in Plastics, 2nd ed. vol. 3, J. Peters, Ed.  New York: McGraw-Hill, 1964, pp. 15–64.

[2]	W.-K. Chen, Linear Networks and Systems (Book style).	Belmont, CA: Wadsworth, 1993, pp. 123–135.

[3]	http://mike.verdone.ca/twitter/#development

[4]	https://networkx.github.io/

[5]	http://matplotlib.org/

[6]	http://visjs.org/

[7]	https://gephi.org/

[8]	http://www.ccsr.ac.uk/methods/publications/snacourse/netdata.html
