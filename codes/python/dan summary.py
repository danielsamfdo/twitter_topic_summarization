import re;
import json;
import urllib
import urllib2
from nltk.tokenize import word_tokenize;
from nltk.tag import pos_tag;
from nltk.chunk import ne_chunk
from gensim import corpora, models, similarities

#--------------------------------------
EIcons=[];
Punctuations=[',',';','.']
PHRASES_ALL=[];
Shortforms=[];#short forms of chat language
Fullforms=[];#full forms of corresponding language
#--------------------------------------

def init():
    Emoticons();
    chatwords();

def Emoticons():        #get all the emoticons
    f=open('emoticon1.txt')
    lines=f.readlines();
    for line in lines:
        x=line.split();
        EIcons.append(x[0]);
    f.close();

def EXTRACTINFO(Phrase):
    return "";
        
    

def chatwords():        #get all chat words 
    f=open('abbreviations.txt')
    lines=f.readlines()
    i=0;
    for line in lines:
        x=line.split("\t",1);
        Shortforms.append(x[0]);
        Fullforms.append(x[1]);
    f.close();


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

def tokenize(line,SA):
    Emoticons=findEmoticons(line);
    print Emoticons;
    URL=findURLS(line);
    print URL;
    HASHTAG=findHashTags(line);
    print HASHTAG;
    USERS=findDirectedat(line);
    print USERS;
    print "?><"
    Newline=line.split();
    for x in Newline:
        print x;
        if x in Emoticons:
            Newline.remove(x);
        elif x in HASHTAG:
            Newline.remove(x);
        elif x in URL:
            Newline.remove(x);
        elif x in USERS:
            Newline.remove(x);
    LINE="";
    for x in Newline:
        LINE=LINE+' '+x;
    print LINE;
    print "<>"
    ENTITY=findENTITIES(LINE);
    print ENTITY;
    Phrase=findPHRASES(LINE);
    print "##################";
    print Phrase;
    if SA==4:
        print "Question";
        #INFO_PHRASE=EXTRACTINFO(Phrase);
    PHRASES_ALL.append(Phrase);
    
    Punctuation=findPUNCTUATION(line)
    print Punctuation;
    return "";

def findURLS(line):
    urlpattern=re.compile("((https?://)?www[.][a-z1-9A-Z]*[.](com|in|co[.]uk|org[.]in))");
    match=urlpattern.findall(line)
    return match;

def findHashTags(line):
    urlpattern=re.compile("[ ]#[a-zA-Z0-9]*");
    match=urlpattern.findall(line)
    return match

def findDirectedat(line):
    urlpattern=re.compile("@[a-zA-Z0-9_]+");
    match=urlpattern.findall(line)
    return match;

def findENTITIES(line):
    X=ne_chunk(pos_tag(word_tokenize(line)));
    return X;

def findPHRASES(line):
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
    return phrase;
    #Object=json.dumps(the_page);
    #return Object;

def rankingofphrases(list):
    return "";

#chatwords();
    
#Text="It is of really bad quality :(."
#tokenize(Text);
init();
f = file("tweets.txt", "r")
lines = f.readlines()
#line = f.readline()
for line in lines:
    print line;
tokenize(line,4);
f.close();
"""


documents=['Bjp supported riot','Talks of peace','mobbed to death']
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
dictionary.save('dan.dict');
print dictionary
print dictionary.token2id
#Sample doc
new_doc = "rt @waglenikhil: good decision by kejriwal govt to form sit for 84 riots. will expose both cong n bjp."
new_vec = dictionary.doc2bow(new_doc.lower().split())
print new_vec
#serialize corpora
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('dan.mm', corpus)
print corpus


class MyCorpus(object):
	def __iter__(self):
		for line in open('mycorpus.txt'):
			 yield dictionary.doc2bow(line.lower().split())
corpus_memory_friendly = MyCorpus()
print corpus_memory_friendly

for vector in corpus_memory_friendly:
    print vector

#Filtering stop words and compacting the dictionary
dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()
print dictionary

#Model Transformation
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
corpus_lsi = lsi[corpus_tfidf]
lsi.print_topics(2)
lsi.save('model.lsi')
lsi = models.LsiModel.load('model.lsi')

#TEST
doc =documents[2] 
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]
print vec_lsi

#INDEX
index = similarities.MatrixSimilarity(lsi[corpus])
index.save('dan.index')
index = similarities.MatrixSimilarity.load('dan.index');
sims = index[vec_lsi]
print list(enumerate(sims))
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print "#################"
print sims
"""
