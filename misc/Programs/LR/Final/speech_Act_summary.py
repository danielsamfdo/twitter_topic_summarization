import re;
import json;
import urllib
import urllib2
import time
from nltk.tokenize import word_tokenize;
from nltk.tag import pos_tag;
import nltk;
from nltk.chunk import ne_chunk
from gensim import corpora, models, similarities
import enchant
#------------------------------------------------
pi=0.25;
tau=0.01;
English_Checker=enchant.Dict('en_US');
tweet_file="JE.txt";
#-------------------------------------------------
EIcons=[];
Punctuations=[',',';','.']
PHRASES_ALL=[];
TEXT=[];
Shortforms=[];      #short forms of chat language
Fullforms=[];       #full forms of corresponding language
tweets_text = []    # We will store the text of every tweet in this list
tweets_rtcnt = []   # Location of every tweet (free text field - not always accurate or given)
tweets_created_at=[]
URLPATTERN="(https?://(www[.])?[a-z0-9A-Z]+[.](com|in|co[.]uk|org[.]in|co)/[a-zA-Z0-9]*)";
HASHPATTERN="#[a-zA-Z0-9]*";
USERPATTERN="@[a-zA-Z0-9_]+";
#--------------------------------------
def ListPrint(SampleList):
    for i in SampleList:
        print i;
    print "<-------------------------->"

def train_split():
    f=open(tweet_file);
    f1=open("1.txt","w");
    f2=open("11.txt","w");
    lines=f.readlines();
    for line in lines:
        t1=line.split('::');
        if(t1[1]==' sta\n'):
            f2.write('1\n');
        elif(t1[1]==' que\n'):
            f2.write('2\n');
        elif(t1[1]==' mis\n'):
            f2.write('4\n');
        else:
            f2.write('3\n');
        f1.write(t1[0]+'\n');
    f.close();
    f1.close();
    f2.close();

#train_split();

def init():
    train_split();
    print "Loadin Emoticons"
    Emoticons();
    print "Loadin Chat words"
    chatwords();
    print "Extracting Tweets from Json Format ";
    JsonExtract();

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

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


def Emoticons():        #get all the emoticons
    f=open('emoticon1.txt')
    lines=f.readlines();
    for line in lines:
        x=line.split();
        EIcons.append(x[0]);
    f.close();

def chatwords():        #get all chat words 
    f=open('abbreviations.txt')
    lines=f.readlines()
    i=0;
    for line in lines:
        x=line.split("\t",1);
        Shortforms.append(x[0]);
        Fullforms.append(x[1][:len(x[1])-1]);
    f.close();

def abbrev(line):
    line_edit=re.sub("&amp;","&",line);
    Newline="";
    x=line_edit.split();
    for j in x:
        if j in Shortforms:
            Newline+=" "+Fullforms[Shortforms.index(j)];
        else:
            Newline+=" "+j;
    return Newline

def findEmoticons(line):    
    E=[];
    for x in EIcons:
        if x in line:
            E.append(x);
    return E;

def findPUNCTUATION(line):
    E=[];
    for x in Punctuations:
        if x in line:
            E.append(x);
    return E;

def tokenize_TEXT(line):
    Emoticons=findEmoticons(line);
    #print Emoticons;
    URL=findURLS(line);
    #print URL;
    HASHTAG=findHashTags(line);
    #print HASHTAG;
    USERS=findDirectedat(line);
    #print USERS;
    #print "?><"
    Newline=line.split();
    LINE="";
    for x in Newline:
        if x in Emoticons:
            Newline.remove(x);
        else:
            LINE+=' '+x;
    LINE=re.sub(URLPATTERN,"",LINE)
    LINE=re.sub(HASHPATTERN,"",LINE)
    LINE=re.sub(USERPATTERN,"",LINE)
    LINE=re.sub("retweet :","",LINE)
    ENTITY=extract_entities(LINE);
    Punctuation=findPUNCTUATION(line)
    List=[];
    List.append(URL);
    List.append(HASHTAG);
    List.append(USERS);
    List.append(Punctuation);
    List.append(LINE);
    List.append(ENTITY);
    return List;

def tokenize(line,SA,TEXT_USE):
    Emoticons=findEmoticons(line);
    #print Emoticons;
    URL=findURLS(line);
    #print URL;
    HASHTAG=findHashTags(line);
    #print HASHTAG;
    USERS=findDirectedat(line);
    #print USERS;
    #print "?><"
    Newline=line.split();
    LINE="";
    for x in Newline:
        if x in Emoticons:
            Newline.remove(x);
        else:
            LINE+=' '+x;
    LINE=re.sub(URLPATTERN,"",LINE)
    LINE=re.sub(HASHPATTERN,"",LINE)
    LINE=re.sub(USERPATTERN,"",LINE)
    LINE=re.sub("retweet :","",LINE)
    TEXT_USE.append(LINE);
    ENTITY=extract_entities(LINE);
    if SA==4:
        print "Question";
    Punctuation=findPUNCTUATION(line)
    List=[];
    List.append(URL);
    List.append(HASHTAG);
    List.append(USERS);
    List.append(Punctuation);
    List.append(LINE);
    List.append(ENTITY);
    return List;

def findURLS(line):
    urlpattern=re.compile("(https?://(www[.])?[a-z0-9A-Z]+[.](com|in|co[.]uk|org[.]in|co)/[a-zA-Z0-9]*)");
    match=urlpattern.findall(line)
    return match;

def findHashTags(line):
    urlpattern=re.compile("#[a-zA-Z0-9]*");
    match=urlpattern.findall(line)
    return match

def findDirectedat(line):
    urlpattern=re.compile("@[a-zA-Z0-9_]+");
    match=urlpattern.findall(line)
    return match;

def findENTITIES(line):
    X=(pos_tag(word_tokenize(line)));
    L=[];
    for i in X:
        if(i[1]=='NNP' or i[1]=='NN'):
            L.append(i[0])
    return L;

def extract_entities(text):
    list_ent=[];
    m='';
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'node'):
                print chunk.node, ' '.join(c[0] for c in chunk.leaves())
                m+=chunk.node;
                for c in chunk.leaves():
                    print c[0];
                    list_ent.append(m+c[0]);
                
    return list_ent;

def findPHRASES(line):
    PHRASES=[]
    try:
        url="http://text-processing.com/api/phrases/"
        values = {'text' : line}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        Object=json.loads(the_page);
        maxlen=-1;
        for x in Object['NP']:
            if(len(x)>maxlen):
                phrase=x;
                maxlen=len(x);
        print "PHRASE ::::::"
        PHRASES.append(phrase);
    except:
        print "Packet for phrase extraction not received";
    return PHRASES;

def JsonExtract():
    # Input argument is the filename of the JSON ascii file from the Twitter API
    filename ="2.json";
    iter=0;
    # Loop over all lines
    for line in open(filename):
        try:
                if(iter>200):
                    break;
                tweet = json.loads(line)
                text = tweet["text"]
                if(is_ascii(text)):
                    if tweet.has_key("retweeted_status"):
                        tweets_rtcnt.append(tweet["retweeted_status"]["retweet_count"]);
                    else:
                        tweets_rtcnt.append(0);
                    tweets_text.append( abbrev(text).lower() )
                    L=Month(tweet["created_at"][4:7])+tweet["created_at"][7:10]
                    tweets_created_at.append(L + tweet["created_at"][25:] +tweet["created_at"][10:19])
                iter+=1;
        except ValueError:
                pass
    x1=tweets_created_at;
    thefile=open('tweetsTEXT.txt','w+');
    for line in tweets_text:
        print>>thefile, line
    thefile.close()
    thefile=open('tweetsRTCNT.txt','w+');
    for line in tweets_rtcnt:
        print>>thefile, line
    thefile.close()
    thefile=open('tweetsTIME.txt','w+');
    for line in tweets_created_at:
        print>>thefile, line
    thefile.close()

#---------PART 1---------------_
JsonExtract();
#_---------PART 2---------------_
#EXECUTE SVM & LR befor progressing
    
def topic(dictionary,prev):
    string="";
    for i in prev:
        string+=dictionary[i]+" ";
    return string

def subtopicdetection(tfidf,corpus,dictionary,TEXTS,IDF_limit):
    c=0;
    TOPICS=[];
    corpus_tfidf = tfidf[corpus]
    index=similarities.MatrixSimilarity(tfidf[corpus]);
    topic_cntr=0;
    XL=[];
    g=0;
    NOOFTWEETS=200;             #differs based on no of tweets
    while(g<len(dictionary)):
        XL.append(0);   
        g+=1
    for d in corpus_tfidf:
        for i in d:
            XL[int(i[0])]+=1;
    print XL    
    #IDF_limit=0.5;
    prev=[];
    for d in corpus_tfidf:
        L=[];
        g=0;
        Wordindoc=[];
        while(g<len(dictionary)):
            L.append(0);
            g+=1
        x=d;
        for i in x:
            L[i[0]]+=1
            if(i[1]>IDF_limit or XL[int(i[0])]>(NOOFTWEETS/15.0)):
                    topic_cntr+=1;
                    Wordindoc.append(dictionary[i[0]]);
            
        if(topic_cntr>=2):       #At the end if the else part isnt executed for the last word   //two or more continuous words found profoundly in a document
            line_split=TEXTS[c].split();
            adj=0;
            for j in line_split:
                if(j in Wordindoc):
                    adj+=1
                else:
                    if(adj>=2):
                        try:
                            if(line_split[line_split.index(j)+adj-1] in ['the','a','an']):    
                                #print line_split[line_split.index(j):line_split.index(j)+adj-1];
                                TOPICS.append(line_split[line_split.index(j):line_split.index(j)+adj-1]);
                            else:
                                TOPICS.append(line_split[line_split.index(j):line_split.index(j)+adj]);
                        except:
                                print "List index out of Range";
                    adj=0
        c+=1;
    return TOPICS;

def summary(tfidf,corpus,dictionary,TEXTS):
    c=0
    Summ=[];
    corpus_tfidf = tfidf[corpus]
    index=similarities.MatrixSimilarity(tfidf[corpus])
    for d in corpus_tfidf:
            L=[];
            g=0;
            while(g<len(dictionary)):
                    L.append(0);
                    g+=1
            x=d;
            for i in x:
                    #print dictionary[i[0]]
                    L[i[0]]+=1
            #print "........"+str(c)
            sims = index[d]
            #print sims;
            j=0;
            togg=0;                                     
            while(j<c):                             #Check if similar to the before texts
                    #print j,sims[j]
                    if(sims[j]>0.8):
                            togg=1;
                            #print c;
                            #print "sadsfasdf"
                            break;
                    j+=1;
            
            if(togg==0):
                    Summ.append(TEXTS[c]);
            c+=1
    return Summ;

def EntitySummary(tfidf,corpus,dictionary,TEXTS):
    c=0
    Summ=[];
    LIST=[];
    corpus_tfidf = tfidf[corpus]
    index=similarities.MatrixSimilarity(tfidf[corpus])
    for d in TEXTS:
            X=(pos_tag(word_tokenize(d)));
            L=[];
            if(d not in Summ):
                for i in X:
                    if(i[1]=='NNP'):
                        Summ.append(d);
                        break;
                    elif(i[1]=='CD'):
                        Summ.append(d);
                        break;
                        
    return Summ;

STOPLIST=['from','i','he','she','it','is','of','lol']

def Scrutiny(domain,L):
    LIST=[];
    for i in L:
            if(i[0] in STOPLIST):
                    i.remove(i[0])
            if(i[len(i)-1] in STOPLIST):
                    i.remove(i[len(i)-1]);
            for j in i:
                    if(j in STOPLIST):
                            i.remove(j);
            if(len(i)>=2):
                    for j in i:
                            if(j in domain):
                                    if(i not in LIST):
                                        LIST.append(i);
                                    break;
    return LIST


def Test_Summary(): #Text in tweets_text
    TEXT=[];
    TEXT_TIME=[];
    MEGA_INFO=[];
    f=open('Test_classification.txt')
    iter=0;
    while(iter<=4):
        f.readline();
        iter+=1;
    iter=0;
    while(iter<len(tweets_text)):
        line=f.readline()
        if(len(line)==0):
            break;
        x=int(line[len(line)-2]);
        print x;
        if(x in [1,2,3]): #if x is not miscelaneous
            TEXT.append(tweets_text[iter]);
            TEXT_TIME.append(tweets_created_at[iter])
        iter+=1
    print TEXT;
    SUB_TOPICS=[];
    print "<=================SPEECH ACT===================>"
    ListPrint(TEXT);
    print "<#########################################>"
    for i in TEXT:
        C=tokenize_TEXT(i);
        
        MEGA_INFO.append(C);
    print MEGA_INFO
    domain=['bjp','aap']
    TEXT1=[];
    stoplist = set('for a of the and to in an &amp; .'.split())
    texts = [[word for word in document.lower().split() if ((word not in stoplist)and(English_Checker.check(word) or word in domain))]
            for document in TEXT]
    print "TEXTS";
    all_tokens = sum(texts, [])
    
    tokens_once =[''] #set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
            for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('dan.dict');
    print "<----------------------DICTIONARY----------------------->"
    iterator=0;
    while(iterator<len(dictionary)):
        print dictionary[iterator];
        iterator+=1;
    print "<#########################################>"
    #texts=[['people',  'strong', 'administrative', 'experience', 'join', 'bjp', 'join', 'aap.'], ['mumbai', 'police', 'commissioner',  'resigns,', 'may', 'join', 'bjp'], ['mumbai', 'police', 'commissioner', 'resigns,', 'may', 'join', 'bjp'], ['join', 'bjp'], [ 'counter',  'join', 'bjp'], [ 'police', 'chief', 'resigns,', 'may', 'join', 'fight', 'lok', 'sabha', 'polls.', 'also', 'joins', '.']]
    dictionary = corpora.Dictionary(texts)
    M=[];
    for i in TEXT:
            M.append(i.split());
    corpus = [dictionary.doc2bow(text) for text in M]
    tfidf = models.TfidfModel(corpus)
    L=[];
    L=(subtopicdetection(tfidf,corpus,dictionary,TEXT,0.3));
    print "Subtopics detected in Validation Set 3 Are:"
    ListPrint(L);
    print "<#########################################>"
    print "<====AFTER Scrutinity=====>"
    LIST_Scrut=Scrutiny(domain,L)
    ListPrint(Scrutiny(domain,L));
    print "<#########################################>"
    print "A plain Summary of Validation Set 1 is:"
    if(len(subtopicdetection(tfidf,corpus,dictionary,TEXT,0.3))==0):
        print "<======================ENTITY SUMMARY==============================>"
        ListPrint(EntitySummary(tfidf,corpus,dictionary,TEXT));
    else:
        ListPrint(summary(tfidf,corpus,dictionary,TEXT));
    print "<############END OF VALIDATION SET 1###################>";

Test_Summary()
def STD_Validation_1():
    print "<############START OF VALIDATION SET 1###################>";
    DOCS=["retweet @simblee: @bhupendrachaube people with strong administrative experience join bjp. the farters join aap.",
    "retweet @indiatoday: mumbai police commissioner satyapal singh resigns, may join bjp http://t.co/angaxnuxbi",
    "retweet @indiatoday: mumbai police commissioner satyapal singh resigns, may join bjp http://t.co/angaxnuxbi",
    "hahahaha. bappi da, be laabh euuu @ani_news: bappi lahiri to join bjp",
    "pappi lahiri to counter \"lovely\" singh :) rt: @ani_news bappi lahiri to join bjp",
    "#sochoindia: #mumbai police chief resigns, may join #bjp to fight lok sabha polls. bappi lahri also joins #bjp."
    ]
    print "<------------DOCUMENTS IN VALIDATION SET 1------------------>"
    ListPrint(DOCS);
    domain=['bjp','aap','lahiri','bappi','pappi','lok','sabha','satyapal','singh']
    TEXT1=[];
    for i in DOCS:
        tokenize(i,"",TEXT1);
    print "<--------------PROCESSED DOCUMENTS--------------->"
    ListPrint(TEXT1);
    stoplist = set('for a of the and to in an .'.split())

    texts = [[word for word in document.lower().split() if ((word not in stoplist)and(English_Checker.check(word) or word in domain))]
            for document in TEXT1]
    print "TEXTS";
    all_tokens = sum(texts, [])

    tokens_once =[''] #set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
            for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('dan.dict');
    print "<----------------------DICTIONARY----------------------->"
    iterator=0;
    while(iterator<len(dictionary)):
        print dictionary[iterator];
        iterator+=1;
    #texts=[['people',  'strong', 'administrative', 'experience', 'join', 'bjp', 'join', 'aap.'], ['mumbai', 'police', 'commissioner',  'resigns,', 'may', 'join', 'bjp'], ['mumbai', 'police', 'commissioner', 'resigns,', 'may', 'join', 'bjp'], ['join', 'bjp'], [ 'counter',  'join', 'bjp'], [ 'police', 'chief', 'resigns,', 'may', 'join', 'fight', 'lok', 'sabha', 'polls.', 'also', 'joins', '.']]
    dictionary = corpora.Dictionary(texts)
    M=[];
    for i in TEXT1:
            M.append(i.split());
    corpus = [dictionary.doc2bow(text) for text in M]
    tfidf = models.TfidfModel(corpus)
    L=[];
    print "Subtopics detected in Validation Set 1 Are:"
    ListPrint(subtopicdetection(tfidf,corpus,dictionary,TEXT1,0.4));
    print "A plain Summary of Validation Set 1 is:"
    ListPrint(summary(tfidf,corpus,dictionary,TEXT1));
    print "<############END OF VALIDATION SET 1###################>";

def SA_SUMM_MAIN(doc_to_summ):
    i=0;
    while(i<len(doc_to_summ)):
        line=doc_to_summ[i];
        speechact=doc_to_summ[i+1];
        if(speechact==1):
            print findPHRASES(line);
        i+=2;

def SPEECH_ACT_Summary(DOCS,X):
    i=0;
    doc_to_summ=[];
    while(i<len(X)):
        if(X[i]==1):
            doc_to_summ.append(DOCS[i]);
            doc_to_summ.append(X[i]);
        i+=1;
    print "<-PHRASE SUMMARY->"
    SA_SUMM_MAIN(doc_to_summ);
    print "<---------------->"
    return doc_to_summ;

def STD_Validation_2():
    print "<############START OF VALIDATION SET 2###################>";
    DOCS=[u"  i want to hang out with a chill tiger right now. or just a chill person, i'm lonely.", u' kingston ssdnow v300 120gb sataiii solid state drive $59.99 at tigerdirect: tiger direct coupons ', u' between 1902 and 1907 the same tiger killed 436 people in india.', u' former tiger  representing clemson with his memories of the combine.   ', u' designer womens watches tiger bracelet.silver 925 japan: price 155.0 usd (0 bids) end time: 2014-02-20 04:11:27 pdt ', u' download now triumph tiger 900 885cc parent has left 00 service repair workshop manual download: this is a complete service... ', u' i believe the products i love should be free from tiger extinction. join me! together whatever can  '];
    X=[2,1,1,2,1,1,1,2];
    print "<---------------DOCUMENTS IN VALIDATION SET 1------------------>"
    ListPrint(DOCS);
    print "<=================SPEECH ACT===================>"
    ListPrint(SPEECH_ACT_Summary(DOCS,X));
    MEGA_INFO=[];
    for i in DOCS:
        C=tokenize(i,"",TEXT);
        c1=[];
        try:
            m=tweets_created_at[tweets_text.index(i)]
            c1.append(m[len(m)-8:len(m)]);
            C.append(c1);
        except:
            C.append(c1);
        MEGA_INFO.append(C);

    domain=[]
    TEXT1=[];
    for i in DOCS:
        tokenize(i,"",TEXT1);
    print "<--------------PROCESSED DOCUMENTS--------------->"
    ListPrint(TEXT1);
    stoplist = set('for a of the and to in an .'.split())
    texts = [[word for word in document.lower().split() if ((word not in stoplist)and(English_Checker.check(word) or word in domain))]
            for document in TEXT1]
    print "TEXTS";
    all_tokens = sum(texts, [])
    
    tokens_once =[''] #set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
            for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('dan.dict');
    print "<----------------------DICTIONARY----------------------->"
    iterator=0;
    while(iterator<len(dictionary)):
        print dictionary[iterator];
        iterator+=1;
    #texts=[['people',  'strong', 'administrative', 'experience', 'join', 'bjp', 'join', 'aap.'], ['mumbai', 'police', 'commissioner',  'resigns,', 'may', 'join', 'bjp'], ['mumbai', 'police', 'commissioner', 'resigns,', 'may', 'join', 'bjp'], ['join', 'bjp'], [ 'counter',  'join', 'bjp'], [ 'police', 'chief', 'resigns,', 'may', 'join', 'fight', 'lok', 'sabha', 'polls.', 'also', 'joins', '.']]
    dictionary = corpora.Dictionary(texts)
    M=[];
    for i in TEXT1:
            M.append(i.split());
    corpus = [dictionary.doc2bow(text) for text in M]
    tfidf = models.TfidfModel(corpus)
    L=[];
    print "Subtopics detected in Validation Set 1 Are:"
    ListPrint((subtopicdetection(tfidf,corpus,dictionary,TEXT1,0.4)));
    print "A plain Summary of Validation Set 1 is:"
    if(len(subtopicdetection(tfidf,corpus,dictionary,TEXT1,0.4))==0):
        print "<======================ENTITY SUMMARY==============================>"
        ListPrint(EntitySummary(tfidf,corpus,dictionary,TEXT1));
    else:
        ListPrint(summary(tfidf,corpus,dictionary,TEXT1));
    print "<############END OF VALIDATION SET 1###################>";

def STD_Validation_2():
    print "<############START OF VALIDATION SET 2###################>";
    DOCS=[u"  i want to hang out with a chill tiger right now. or just a chill person, i'm lonely.", u' kingston ssdnow v300 120gb sataiii solid state drive $59.99 at tigerdirect: tiger direct coupons ', u' between 1902 and 1907 the same tiger killed 436 people in india.', u' former tiger  representing clemson with his memories of the combine.   ', u' designer womens watches tiger bracelet.silver 925 japan: price 155.0 usd (0 bids) end time: 2014-02-20 04:11:27 pdt ', u' download now triumph tiger 900 885cc parent has left 00 service repair workshop manual download: this is a complete service... ', u' i believe the products i love should be free from tiger extinction. join me! together whatever can  '];
    X=[2,1,1,2,1,1,1,2];
    print "<---------------DOCUMENTS IN VALIDATION SET 1------------------>"
    ListPrint(DOCS);
    print "<#########################################>"
    print "<=================SPEECH ACT===================>"
    ListPrint(SPEECH_ACT_Summary(DOCS,X));
    print "<#########################################>"
    MEGA_INFO=[];
    for i in DOCS:
        C=tokenize(i,"",TEXT);
        c1=[];
        try:
            m=tweets_created_at[tweets_text.index(i)]
            c1.append(m[len(m)-8:len(m)]);
            C.append(c1);
        except:
            C.append(c1);
        MEGA_INFO.append(C);

    domain=[]
    TEXT1=[];
    for i in DOCS:
        tokenize(i,"",TEXT1);
    print "<--------------PROCESSED DOCUMENTS--------------->"
    ListPrint(TEXT1);
    print "<#########################################>"
    stoplist = set('for a of the and to in an .'.split())
    texts = [[word for word in document.lower().split() if ((word not in stoplist)and(English_Checker.check(word) or word in domain))]
            for document in TEXT1]
    all_tokens = sum(texts, [])
    
    tokens_once =[''] #set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
            for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('dan.dict');
    print "<----------------------DICTIONARY----------------------->"
    iterator=0;
    while(iterator<len(dictionary)):
        print dictionary[iterator];
        iterator+=1;
    print "<#########################################>"
    #texts=[['people',  'strong', 'administrative', 'experience', 'join', 'bjp', 'join', 'aap.'], ['mumbai', 'police', 'commissioner',  'resigns,', 'may', 'join', 'bjp'], ['mumbai', 'police', 'commissioner', 'resigns,', 'may', 'join', 'bjp'], ['join', 'bjp'], [ 'counter',  'join', 'bjp'], [ 'police', 'chief', 'resigns,', 'may', 'join', 'fight', 'lok', 'sabha', 'polls.', 'also', 'joins', '.']]
    dictionary = corpora.Dictionary(texts)
    M=[];
    for i in TEXT1:
            M.append(i.split());
    corpus = [dictionary.doc2bow(text) for text in M]
    tfidf = models.TfidfModel(corpus)
    L=[];
    print "Subtopics detected in Validation Set 1 Are:"
    ListPrint((subtopicdetection(tfidf,corpus,dictionary,TEXT1,0.5)));
    print "<#########################################>"
    print "A plain Summary of Validation Set 1 is:"
    if(len(subtopicdetection(tfidf,corpus,dictionary,TEXT1,0.5))==0):
        print "<======================ENTITY SUMMARY==============================>"
        ListPrint(EntitySummary(tfidf,corpus,dictionary,TEXT1));
    else:
        ListPrint(summary(tfidf,corpus,dictionary,TEXT1));
    print "<#########################################>"
    print "<############END OF VALIDATION SET 1###################>";

def STD_Validation_3():
    print "<############START OF VALIDATION SET 3###################>";
    DOCS=[u' almost 3 months after his retirement, sachin tendulkar sets another cricketing record ---&gt; ', u' sachin trendulkar*  out of top 5 tweeets of ... to are mine i feel like sachin tendulakar now :p ', u' 54 members retire from the rajya sabha. while sachin tendulkar looks on nervously.', u' 54 members retire from the rajya sabha. while sachin tendulkar looks on nervously.', u'  the only thing i wud worry about wud be that..is sachin going to score a century today! ', u" from our archives, youth connect's tribute to sachin tendulkar. hey must read story about the life and the legend... ", u'   the only thing i wud worry about wud be that..is sachin going to score a century today! ', u' i just got a personalized digital autograph from sachin tendulkar & .  to get yours twitter post  .', u' yes, he is a good player. but now, if he become a captain of test match. it may harm his performance. ', u" icc's regular 50 overs world cup without sachin is as hard to imagine as  is without shahid afridi jokes.", u' fake facebook wall...virat kohli wants to break all records of sachin tendulkar :p ', u' virat kohli is a combination of sachin, sehwag and dravid: martin crowe - the times of india ', u' is virat kohli the next sachin tendulkar? - the times of india ', u' ', u' post by sachin arakeri: in a parallel comicverse! ', u'   i want to play cricket with sir sachin tendulkar', u'  bating - sachin,sourav,adam,veeru,yuvi,clarke,dravid laxman (test match only) bowler - lee,sohaib,mc grath long list lol :p', u'  54 members retire from the rajya sabha. while sachin tendulkar looks on nervously.', u'  how old were they when sachin started his career ? '];
    X=[3,1,2,1,1,2,2,2,1,2,2,2,1,3,4,1,2,4,1,3];
    print "<---------------DOCUMENTS IN VALIDATION SET 1------------------>"
    ListPrint(DOCS);
    print "<#########################################>"
    print "<=================SPEECH ACT===================>"
    ListPrint(SPEECH_ACT_Summary(DOCS,X));
    print "<#########################################>"
    MEGA_INFO=[];
    for i in DOCS:
        C=tokenize(i,"",TEXT);
        c1=[];
        try:
            m=tweets_created_at[tweets_text.index(i)]
            c1.append(m[len(m)-8:len(m)]);
            C.append(c1);
        except:
            C.append(c1);
        MEGA_INFO.append(C);

    domain=['sachin','tendulkar','virat','kohli','dravid','laxman']
    TEXT1=[];
    for i in DOCS:
        tokenize(i,"",TEXT1);
    print "<--------------PROCESSED DOCUMENTS--------------->"
    ListPrint(TEXT1);
    print "<#########################################>"
    stoplist = set('for a of the and to in an .'.split())
    texts = [[word for word in document.lower().split() if ((word not in stoplist)and(English_Checker.check(word) or word in domain))]
            for document in TEXT1]
    print "TEXTS";
    all_tokens = sum(texts, [])
    
    tokens_once =[''] #set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
            for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('dan.dict');
    print "<----------------------DICTIONARY----------------------->"
    iterator=0;
    while(iterator<len(dictionary)):
        print dictionary[iterator];
        iterator+=1;
    print "<#########################################>"
    #texts=[['people',  'strong', 'administrative', 'experience', 'join', 'bjp', 'join', 'aap.'], ['mumbai', 'police', 'commissioner',  'resigns,', 'may', 'join', 'bjp'], ['mumbai', 'police', 'commissioner', 'resigns,', 'may', 'join', 'bjp'], ['join', 'bjp'], [ 'counter',  'join', 'bjp'], [ 'police', 'chief', 'resigns,', 'may', 'join', 'fight', 'lok', 'sabha', 'polls.', 'also', 'joins', '.']]
    dictionary = corpora.Dictionary(texts)
    M=[];
    for i in TEXT1:
            M.append(i.split());
    corpus = [dictionary.doc2bow(text) for text in M]
    tfidf = models.TfidfModel(corpus)
    L=[];
    print "Subtopics detected in Validation Set 1 Are:"
    ListPrint((subtopicdetection(tfidf,corpus,dictionary,TEXT1)));
    print "<#########################################>"
    print "A plain Summary of Validation Set 1 is:"
    if(len(subtopicdetection(tfidf,corpus,dictionary,TEXT1))==0):
        print "<======================ENTITY SUMMARY==============================>"
        ListPrint(EntitySummary(tfidf,corpus,dictionary,TEXT1));
    else:
        ListPrint(summary(tfidf,corpus,dictionary,TEXT1));
    print "<############END OF VALIDATION SET 1###################>";

def Concat(j):
    b="";
    togg=0;
    for i in j:
        if(togg==0):
            togg=1;
            b+=i;
        else:
            b+=" "+i;
    return b;

def FILEWRITE(fname,LIST):
    f=open(fname,'w');
    for line in LIST:
        f.write(line+'\n');
    f.close();

def SplitintoBuckets(texts,domain,LIST):
    documents=[]
    FILEWRITE('mycorpus1.txt',LIST);
    docs=texts;
    for i in docs:
        documents.append(Concat(i))
    #set of stop words
    stoplist = set('for a of the and to in'.split())

    texts = [[word for word in document.lower().split() if word not in stoplist]
            for document in documents]

    all_tokens = sum(texts, [])

    tokens_once =[''] #set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

    texts = [[word for word in text if word not in tokens_once]
            for text in texts]

    print texts

    #Save Dictionary
    dictionary = corpora.Dictionary(texts)
    #dictionary.save('dan.dict');
    #print dictionary
    print dictionary.token2id
    #serialize corpora
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('dan.mm', corpus)
    print corpus

    #Filtering stop words and compacting the dictionary
    dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus1.txt'))
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids)
    dictionary.compactify()
    print dictionary

    #Model Transformation LSA
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
    corpus_lsi = lsi[corpus_tfidf]
    lsi.print_topics(2)
    #lsi.save('model.lsi')
    #lsi = models.LsiModel.load('model.lsi')

    Bucket_List=[];
    for i in docs:
        Bucket_List.append([]);
    #TEST
    for doc in open('mycorpus1.txt'):
        vec_bow = dictionary.doc2bow(doc.lower().split())
        vec_lsi = lsi[vec_bow]
        print vec_lsi
        print doc;
        print "latent semantic indexing for the above doc "
        #INDEX
        index = similarities.MatrixSimilarity(lsi[corpus])
        #index.save('dan.index')
        #index = similarities.MatrixSimilarity.load('dan.index');
        sims = index[vec_lsi]
        print list(enumerate(sims))
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        print "#################"
        docx=sims[0];
        if(docx[1]>0.9):
            print documents[docx[0]];
            print docx[0];
            #time.sleep(5);
            Bucket_List[int(docx[0])].append(doc);
        else:
            print "not added";
    print Bucket_List;


def STD_Validation_3():
    print "<############START OF VALIDATION SET 3 TESTING ###################>";
    DOCS=[u' almost 3 months after his retirement, sachin tendulkar sets another cricketing record ---&gt; ', u' sachin trendulkar*  out of top 5 tweeets of ... to are mine i feel like sachin tendulakar now :p ', u' 54 members retire from the rajya sabha. while sachin tendulkar looks on nervously.', u' 54 members retire from the rajya sabha. while sachin tendulkar looks on nervously.', u'  the only thing i wud worry about wud be that..is sachin going to score a century today! ', u" from our archives, youth connect's tribute to sachin tendulkar. hey must read story about the life and the legend... ", u'   the only thing i wud worry about wud be that..is sachin going to score a century today! ', u' i just got a personalized digital autograph from sachin tendulkar & .  to get yours twitter post  .', u' yes, he is a good player. but now, if he become a captain of test match. it may harm his performance. ', u" icc's regular 50 overs world cup without sachin is as hard to imagine as  is without shahid afridi jokes.", u' fake facebook wall...virat kohli wants to break all records of sachin tendulkar :p ', u' virat kohli is a combination of sachin, sehwag and dravid: martin crowe - the times of india ', u' is virat kohli the next sachin tendulkar? - the times of india ', u' ', u' post by sachin arakeri: in a parallel comicverse! ', u'   i want to play cricket with sir sachin tendulkar', u'  bating - sachin,sourav,adam,veeru,yuvi,clarke,dravid laxman (test match only) bowler - lee,sohaib,mc grath long list lol :p', u'  54 members retire from the rajya sabha. while sachin tendulkar looks on nervously.', u'  how old were they when sachin started his career ? '];
    X=[3,1,2,1,1,2,2,2,1,2,2,2,1,3,4,1,2,4,1,3];
    print "<---------------DOCUMENTS IN VALIDATION SET 1------------------>"
    ListPrint(DOCS);
    print "<#########################################>"
    print "<=================SPEECH ACT===================>"
    ListPrint(SPEECH_ACT_Summary(DOCS,X));
    MEGA_INFO=[];
    for i in DOCS:
        C=tokenize(i,"",TEXT);
        c1=[];
        try:
            m=tweets_created_at[tweets_text.index(i)]
            c1.append(m[len(m)-8:len(m)]);
            C.append(c1);
        except:
            C.append(c1);
        MEGA_INFO.append(C);

    domain=['sachin','tendulkar','virat','kohli','dravid','laxman']
    TEXT1=[];
    for i in DOCS:
        tokenize(i,"",TEXT1);
    print "<--------------PROCESSED DOCUMENTS--------------->"
    ListPrint(TEXT1);
    print "<#########################################>"
    stoplist = set('for a of the and to in an .'.split())
    texts = [[word for word in document.lower().split() if ((word not in stoplist)and(English_Checker.check(word) or word in domain))]
            for document in TEXT1]
    all_tokens = sum(texts, [])

    tokens_once =[''] #set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
            for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('dan.dict');
    print "<----------------------DICTIONARY----------------------->"
    iterator=0;
    while(iterator<len(dictionary)):
        print dictionary[iterator];
        iterator+=1;
    print "<#########################################>"
    dictionary = corpora.Dictionary(texts)
    M=[];
    for i in TEXT1:
            M.append(i.split());
    corpus = [dictionary.doc2bow(text) for text in M]
    tfidf = models.TfidfModel(corpus)
    L=(subtopicdetection(tfidf,corpus,dictionary,TEXT1,0.32));
    print "Subtopics detected in Validation Set 3 Are:"
    ListPrint(L);
    print "<#########################################>"
    print "<====AFTER Scrutinity=====>"
    LIST_Scrut=Scrutiny(domain,L)
    ListPrint(Scrutiny(domain,L));
    print "<#########################################>"
    print "split into buckets /_________________________/"
    BucSPLIT=SplitintoBuckets(Scrutiny(domain,L),domain,DOCS);
    print BucSPLIT;
    print "<#########################################>"
    print "A plain Summary of Validation Set 3 is:"
    if(len(subtopicdetection(tfidf,corpus,dictionary,TEXT1,0.32))==0):
        print "<======================ENTITY SUMMARY==============================>"
        ListPrint(EntitySummary(tfidf,corpus,dictionary,TEXT1));
    else:
        ListPrint(summary(tfidf,corpus,dictionary,TEXT1));
                
    print "<############END OF VALIDATION SET 1###################>";

def STD_Validation_11():
    print "<############START OF VALIDATION SET 1###################>";
    DOCS=[]
    for i in TEXT[:200]:
        DOCS.append(i);
    print "<------------DOCUMENTS IN VALIDATION SET 1------------------>"
    ListPrint(DOCS);
    domain=['bjp','aap','lahiri','bappi','pappi','lok','sabha','satyapal','singh']
    TEXT1=[];
    for i in DOCS:
        tokenize(i,"",TEXT1);
    print "<--------------PROCESSED DOCUMENTS--------------->"
    ListPrint(TEXT1);
    stoplist = set('for a of the and to in an .'.split())

    texts = [[word for word in document.lower().split() if ((word not in stoplist)and(English_Checker.check(word) or word in domain))]
            for document in TEXT1]
    print "TEXTS";
    all_tokens = sum(texts, [])

    tokens_once =[''] #set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
            for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('dan.dict');
    print "<----------------------DICTIONARY----------------------->"
    iterator=0;
    while(iterator<len(dictionary)):
        print dictionary[iterator];
        iterator+=1;
    #texts=[['people',  'strong', 'administrative', 'experience', 'join', 'bjp', 'join', 'aap.'], ['mumbai', 'police', 'commissioner',  'resigns,', 'may', 'join', 'bjp'], ['mumbai', 'police', 'commissioner', 'resigns,', 'may', 'join', 'bjp'], ['join', 'bjp'], [ 'counter',  'join', 'bjp'], [ 'police', 'chief', 'resigns,', 'may', 'join', 'fight', 'lok', 'sabha', 'polls.', 'also', 'joins', '.']]
    dictionary = corpora.Dictionary(texts)
    M=[];
    for i in TEXT1:
            M.append(i.split());
    corpus = [dictionary.doc2bow(text) for text in M]
    tfidf = models.TfidfModel(corpus)
    L=[];
    print "Subtopics detected in Validation Set 1 Are:"
    ListPrint(subtopicdetection(tfidf,corpus,dictionary,TEXT1,0.4));
    print "A plain Summary of Validation Set 1 is:"
    X=summary(tfidf,corpus,dictionary,TEXT1);
    print len(X);
    print "<############END OF VALIDATION SET 1###################>";

def remove_fullstops(word):
    s='';
    for i in word:
        if(i not in ['.','\'','?']):
            s+=i
    return s;

def ie_process(document):
    sentences = nltk.sent_tokenize(document);
    sentences = [nltk.word_tokenize(sent) for sent in sentences];
    sentences = [nltk.pos_tag(sent) for sent in sentences];
    

DOCS=[]
for i in TEXT[:200]:
    DOCS.append(i);
print "<------------DOCUMENTS IN VALIDATION SET 1------------------>"
ListPrint(DOCS);
domain=['bjp','aap','lahiri','bappi','pappi','lok','sabha','satyapal','singh']
TEXT1=[];
for i in DOCS:
    tokenize(i,"",TEXT1);
print "<--------------PROCESSED DOCUMENTS--------------->"
ListPrint(TEXT1);
stoplist = set('for a of the and to in an .'.split())

texts = [[word for word in document.lower().split() if ((word not in stoplist)and(English_Checker.check(word) or word in domain))]
        for document in TEXT1]
print "TEXTS";
all_tokens = sum(texts, [])

tokens_once =[''] #set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
        for text in texts]
TEXTS_MAIN=[];
for list in texts:
    DICT=[];
    for word in list:
        if(English_Checker.check(word)): #if word is  a proper english word add it in dictionary else remove it 
            x=remove_fullstops(word);
            if x not in DICT:
                DICT.append(x);
    if(len(DICT)>0):
        TEXTS_MAIN.append(DICT);
dictionary = corpora.Dictionary(TEXTS_MAIN)
dictionary.save('dan.dict');
print "<----------------------DICTIONARY----------------------->"
iterator=0;
while(iterator<len(dictionary)):
    print dictionary[iterator];
    iterator+=1;
#texts=[['people',  'strong', 'administrative', 'experience', 'join', 'bjp', 'join', 'aap.'], ['mumbai', 'police', 'commissioner',  'resigns,', 'may', 'join', 'bjp'], ['mumbai', 'police', 'commissioner', 'resigns,', 'may', 'join', 'bjp'], ['join', 'bjp'], [ 'counter',  'join', 'bjp'], [ 'police', 'chief', 'resigns,', 'may', 'join', 'fight', 'lok', 'sabha', 'polls.', 'also', 'joins', '.']]
dictionary = corpora.Dictionary(texts)

"""
M=[];
for i in TEXT1:
        M.append(i.split());
corpus = [dictionary.doc2bow(text) for text in M]
tfidf = models.TfidfModel(corpus)
L=[];
L=(subtopicdetection(tfidf,corpus,dictionary,TEXT1,0.32));
print "Subtopics detected in Validation Set 3 Are:"
ListPrint(L);
print "<#########################################>"

print "<====AFTER Scrutinity=====>"
LIST_Scrut=Scrutiny(domain,L)
ListPrint(LISR_Scrut);
X=summary(tfidf,corpus,dictionary,TEXT1);
print len(X);
print "<############END OF VALIDATION SET 1###################>";
"""
def sort(index,no_ofmax,List):
          Sample=[];
          iter=0;
          while(iter<no_ofmax):
              for i in List:
                  Sample.append(i[index]);
              maxi=max(Sample);
              for i in List:
                  if(i[index]==maxi):
                      MAXINDEX=i[0]
              
              #List.remove([MAXINDEX maxi]);

XCNT=[];
iter=0;
while(iter<len(dictionary)):
    XCNT.append(0);
for text1 in TEXT:
    iter=0;
    for m in text1.split():
        while(iter<len(dictionary)):
            if(dictionary[iter]==m):
              XCNT[iter]+=1;
              break;
            iter+=1;
x=[];
iter=0;
while(iter<len(dictionary)):
    x.append([iter,XCNT[iter]]);
    iter+=1;

print x;


STD_Validation_1()
