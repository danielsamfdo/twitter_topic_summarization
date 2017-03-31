from gensim import corpora, models, similarities

documents = ["Riots",
		"BJP",
		"selection"]
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
doc = "rt @waglenikhil: good decision by kejriwal govt to form sit for 84 riots. will expose both cong n bjp."
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]
print vec_lsi
print doc;
print "latent semantic indexing for the above doc "
#INDEX
index = similarities.MatrixSimilarity(lsi[corpus])
index.save('dan.index')
index = similarities.MatrixSimilarity.load('dan.index');
sims = index[vec_lsi]
print list(enumerate(sims))
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print "#################"
print sims
