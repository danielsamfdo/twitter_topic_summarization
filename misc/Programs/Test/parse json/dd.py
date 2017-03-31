import json
#-------------------------------------------------------------------------------------------------------
pi=0.25;
#---------------

#def OPAD(Stream,DT):
	
#	E,V=Initial(E,V);
#	while(Stream[t]==t(i-1)+DT)<t(n-1):
#		if( (((Mean(t(i))-E)/V) > tau) & Mean(t(i))>Mean(t(i)-DT) ) :
#			tjstart=t(i-1);
#			while((t(i)=t(i-1)+DT)<t(n-1) && (Mean(t(i))>Mean(t(i)-DT))):
#				Update(E,V,Mean(t(i));
#			while(t(i)=t(i-1)+DT)<t(n-1) && (Mean(t(i))>Mean(tjstart)):
#				if(Mean(t(i))-E)/V>tau && Mean(t(i))>Mean(tjstart):
#					tjend=t(i)-DT;
#				else
#					E,V=Update(E,V,Mean(i));
#					tjend=t(i)+DT;



#def Variance(ti,...tj)
#	var of tweet no in (ti+DT,...,tj+DT)

def Initial(E,V):
	E=0;
	V=0;
	return E,V;

def Update(E,V,N):
	Diff=E-N;
	var=pi*Diff+(1-pi)*V;
	mean=pi*N+(1-pi)*E;
	return mean,var;

def Mean(ins):
        if(len(p)>ins):
                return len(p[ins]);
        else:
                return 0;

def no(s):
	m=0;
	return int(s[:2])+int(s[3:5])+int(s[6:]);
def Month(s):
    
    if(cmp("Dec",s)==0):
        return "12"
    elif(cmp("Nov",s)==0):
        return "11"
    elif(cmp("Oct",s)==0):
        return "10"
    elif(cmp("Sep",s)==0):
        return "9"
    elif(cmp("Aug",s)==0):
        return "8"
    elif(cmp("Jul",s)==0):
        return "7"
    elif(cmp("Jun",s)==0):
        return "6"
    elif(cmp("May",s)==0):
        return "5"
    elif(cmp("Apr",s)==0):
        return "4"
    elif(cmp("Mar",s)==0):
        return "3"
    elif(cmp("Feb",s)==0):
        return "2"
    elif(cmp("Jan",s)==0):
        return "1"
    else:
        return "0"

def Add(s1,s2):
    c=0;
    sec=(int(s1[6:])+int(s2[6:]))
    if(sec>60):
        c=1;
    min=int(s1[3:5])+int(s2[3:5])+c;
    if(min>=60):
        min-=60;
        c=1;
    hr=int(s1[:2])+int(s2[:2])+c;
    minute="";second="";hour="";
    if(len(str(sec))<2):
       second="0"
    second+=str(sec);
    if(len(str(min))<2):
       minute="0"
    minute+=str(min);
    if(len(str(hr))<2):
       hour="0"
    hour+=str(hr);
    
    return hour+":"+minute+":"+second;
# Input argument is the filename of the JSON ascii file from the Twitter API
filename ="1.json";

tweets_text = [] # We will store the text of every tweet in this list
tweets_rtcnt = [] # Location of every tweet (free text field - not always accurate or     given)
tweets_created_at=[] 
# Loop over all lines
f = file(filename, "r")
lines = f.readlines()
for line in lines:
    try:
            #print line;
            tweet = json.loads(line)
            text = tweet["text"].lower()
            print tweet["created_at"];
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
            L=Month(tweet["created_at"][4:7])+tweet["created_at"][7:10]
            tweets_created_at.append(L + tweet["created_at"][25:] +tweet["created_at"][10:19])
    except ValueError:
            pass

# Show result
print tweets_text
print tweets_rtcnt
print tweets_created_at
x1=tweets_created_at;

thefile=open('xq.txt','w+');
for line in tweets_text:
    print>>thefile, line
thefile.close()
m=[];
x1.sort();
t=[];
t.append("03:35:00");
DT="00:05:00";
i=0;
while(1):
    x=Add(t[i],DT);
    print x;
    t.append(x);
    i=i+1;
    if(i==14):
        break;
i=1;
print "time"+t[i];
j=0;
p=[];
l=[];
for item in x1:
    
    if(cmp(item[11:],t[i])<0):
        l.append(tweets_text[j]);
        print l;
        j+=1;
    else:
        i+=1;
        p.append(l)
        print p;
        print "time"+t[i];
        l=[];
        j+=1;
p.append(l);
print p;
no_of_tweets=[];
for list in p:
    no_of_tweets.append(len(list));
    print len(list);






