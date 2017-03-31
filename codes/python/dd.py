import json

# Input argument is the filename of the JSON ascii file from the Twitter API
filename ="1.json";

tweets_text = [] # We will store the text of every tweet in this list
tweets_rtcnt = [] # Location of every tweet (free text field - not always accurate or     given)

# Loop over all lines
f = file(filename, "r")
lines = f.readlines()
for line in lines:
    try:
            #print line;
            tweet = json.loads(line)
            text = tweet["text"].lower()
            print text;
            
            if tweet.has_key("retweeted_status"):
                print "retweet:::::"+str(tweet["retweeted_status"]["retweet_count"]);
                tweets_rtcnt.append(tweet["retweeted_status"]["retweet_count"]);
            else:
                tweets_rtcnt.append(0);
            # Ignore 'manual' retweets, i.e. messages starting with RT             
            if text.find("rt ") > -1:
                    continue
            print "--------------------------------";
            tweets_text.append( text )
    except ValueError:
            pass

# Show result
print tweets_text
print tweets_rtcnt
thefile=open('xq.txt','w+');
for line in tweets_text:
    print>>thefile, line
thefile.close()
