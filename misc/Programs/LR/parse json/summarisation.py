import nltk;

def sentence_intersection(sent1,sent2):
    s1=set(sent1.split(" "));
    s2=set(sent2.split(" "));
    print len(s1.intersection(s2));
    if(len(s1.intersection(s2))==0):
        return 0;
    else:
        print "else";
        print len(s1);
        print len(s2);
        return len(s1.intersection(s2))/((len(s1)+len(s2))/2.0);


print sentence_intersection("i like to drive ","he loves to drive ");
