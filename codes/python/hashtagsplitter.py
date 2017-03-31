#opening the file which contains list of words and
#initializing it with a list
#function to initialize the wordlist
def Initializewords():
    with open('hashtagwords.txt') as f:
        content = f.readlines()
    return [word.rstrip('\n') for word in content]
#end of initialization function

def split_hashtag(hashtag,checklist):
    splitted_sentence = ""     
    terms = hashtag.split(' ')
    print(terms)
    for term in terms:
        if term[0] == '#': 
            splitted_sentence += begin_split(term, checklist)
        else: 
            splitted_sentence += term
        splitted_sentence += " "

    return splitted_sentence

def begin_split(term,checklist):
    words = []
    tags = term[1:].split('-')
    print(tags)
    for tag in tags:
        word = FindWord(tag, checklist)    
        while word != None and len(tag) > 0:
            words += [word]            
            """if len(tag) == len(word): 
                break"""
            tag = tag[len(word):]
            word = FindWord(tag, checklist)
    return " ".join(words)

def FindWord(tag, checklist):
    i = len(tag) + 1
    while i > 1:
        i -= 1
        if tag[:i] in checklist:
            return tag[:i]
    return None 


checklist=Initializewords()
hashtag="#factsaboutme"
print(split_hashtag(hashtag,checklist))
