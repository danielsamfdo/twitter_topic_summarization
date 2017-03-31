import nltk
#-----------------------------------------
#global variables
stop=[]
#-----------------------------------------
def getstopwords():
    file1=file("stop.txt","r");
    lines=file1.readlines();
    
    for line in lines:
        print line
        stop.append(line[:len(line)-1]);
    print stop
    print "import completed"
    
def removestopwords(words):
    for x in words:
        if(x in stop):
            print '';
        else:
            print x;
print "##############"

#-----------------------------------------
getstopwords()
#-----------------------------------------
f = file("xxx.txt", "r")
lines = f.readlines()
for line in lines:
    X=line.split(" ");
    Set=set(X);
    words=[];
    for word in Set:
        v='';
        for charac in word:
            if(charac.isalpha()):
                v=v+charac;
            else:
                if(len(v)!=0):
                    words.append(v);
                    v='';
        if(len(v)!=0):
            words.append(v);

        
    print words
    removestopwords(words);
f.close();
                
