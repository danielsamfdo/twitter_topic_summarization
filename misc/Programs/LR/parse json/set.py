import json
import time
#--------------------------------------------------Global Variables-------------------------------------
pi=0.25;
tau=0.01;
#-------------------------------------------------------Functions---------------------------------------

def OPAD(DT,list):
        E,V=0,0;
        E,V=Initial(E,V);
        t=[];
        t.append(list['list'][0]);
        i=1;
        last=t[len(t)-1];
        ti=list['list'][0];
        while(cmp(Add(ti,DT),last)<0):
                tprev=ti;
                ti=Add(ti,DT);
                if(((findCorrect(list,ti,"00:00:00")-E)/V   )>tau   and findCorrect(ti)>findCorrect(list,Sub(ti,DT),"00:00:00") ):
                        tjstart=tprev;
                        while(  cmp(Add(ti,DT),last)<0 and findCorrect(list,ti,"00:00:00")>findCorrect(list,Sub(ti,DT),"00:00:00") ):
                                ti=Add(ti,DT);
                                E,V=Update(E,V,findCorrect(list,ti,"00:00:00"));
                        while(  cmp(Add(ti,DT),last)<0 and findCorrect(list,ti,"00:00:00")>findCorrect(list,tjstart,"00:00:00") ):
                                ti=Add(ti,DT);#added check
                                if((findCorrect(list,ti,"00:00:00")-E)/V)>tau and (findCorrect(list,ti,"00:00:00")>findCorrect(list,ti,"00:00:00")):
                                           tjend=Sub(ti,DT);
                                else:
                                           E,V=Update(E,V,findCorrect(list,ti,"00:00:00"));
                                           tjend=Add(ti,DT);


def findCorrect(list,time1,DT):
        print "in find correct";
        x=Sub(time1,DT);
        print x;
        res=0;
        cnt1=0;
        if(cmp(list['list'][0],time1)>=0):
           return 0;
        print Sub(time1,DT);
        if(cmp(list['list'][0],Sub(time1,DT))>=0):
           return 0;
        else:
                cnt1=list['cnt'][0];
        print cnt1;
        length=len(list['list']);
        i=0;
        while(i<length):
                if(cmp(list['list'][i],Sub(time1,DT))<0):
                        cnt1=list['cnt'][i];
                else:
                        return cnt;
                print cnt1;
                i+=1;
                time.sleep(1)
        return cnt1;
#def Variance(ti,...tj)
#       var of tweet no in (ti+DT,...,tj+DT)

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
    if(sec>=60):
        c=1;
        sec-=60;
    min=int(s1[3:5])+int(s2[3:5])+c;
    if(min>=60):
        min-=60;
        c=1;
    else:
        c=0;
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

def Sub(s1,s2):
    c=0;
    sec=(int(s1[6:])-int(s2[6:]))
    if(sec<0):
        c=1;
        sec=60+(int(s1[6:])-int(s2[6:]));
    min=int(s1[3:5])-int(s2[3:5])-c;
    if(min<0):
        min=60+(int(s1[3:5])-int(s2[3:5])-c);
        c=1;
    else:
        c=0;
    hr=int(s1[:2])-int(s2[:2])-c;
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
#--------------------------------------------------------------------------
# Input argument is the filename of the JSON ascii file from the Twitter API
filename ="1.json";

tweets_text = [] # We will store the text of every tweet in this list
tweets_rtcnt = [] # Location of every tweet (free text field - not always accurate or     given)
tweets_created_at=[] 
# Loop over all lines
f = file(filename, "r")
lines = f.readlines()
print lines
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
            #Ignore 'manual' retweets, i.e. messages starting with RT             
            if text.find("rt ") > -1:
                    continue
            print "--------------------------------";
            tweets_text.append( text )
            L=Month(tweet["created_at"][4:7])+tweet["created_at"][7:10]
            tweets_created_at.append(L + tweet["created_at"][25:] +tweet["created_at"][10:19])
    except ValueError:
            pass

#Show result
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
t.append("03:40:50");
DT="00:00:05";
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
p={'tweets':[],'time':[]};
l=[];
time1=[];
for item in x1:
    
    if(cmp(item[11:],t[i])<0):
        l.append(tweets_text[j]);
        time1.append(item[11:]);
        print l;
        j+=1;
    else:
        i+=1;
        p['tweets'].append(l)
        p['time'].append(time1)
        print p;
        print "time"+t[i];
        l=[];
        j+=1;
p['tweets'].append(l)
p['time'].append(time1)
print p;
no_of_tweets=[];

for list in p:
    no_of_tweets.append(len(list));
    print len(list);
E=0;
V=0;
E,V=Initial(E,V);
cnt=0;
listx={'cnt':[] , 'list':[]  };#for mean(ti-dt)
i=0;
while(i<len(p['time'])):
        for j in p['time'][i]:
                cnt+=1;
                listx['list'].append(j);
                listx['cnt'].append(cnt);
        i+=1;
print Sub("03:40:40","01:02:08")
DT="00:00:20";
print listx
time.sleep(5);
print findCorrect(listx,"03:42:01",DT)
OPAD("00:00:00",listx);
