#---------------import section-------------------#
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

#---------------global variable section-------------------#
English_Checker=enchant.Dict('en_US');
tweet_file="JE.txt";
#---------------Regular Expression---------------#
URLPATTERN="(https?://(www[.])?[a-z0-9A-Z]+[.](com|in|co[.]uk|org[.]in|co)/[a-zA-Z0-9]*)";
HASHPATTERN="#[a-zA-Z0-9]*";
USERPATTERN="@[a-zA-Z0-9_]+";
#------------------------------------------------#
Punctuations=[',',';','.']
Shortforms=[];      #short forms of chat language
Fullforms=[];       #full forms of corresponding language
tweets_text = []    # We will store the text of every tweet in this list
tweets_rtcnt = []   # Location of every tweet (free text field - not always accurate or given)
tweets_created_at=[]

#--------------------FUNCTIONS ------------------#
def ListPrint(SampleList,X):
    print "<------------"+X+"----------------->"
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

train_split();
