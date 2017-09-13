import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag.stanford import StanfordPOSTagger
import contractions as con
import newdata as n
st = StanfordPOSTagger(r'D:/stan/stanford-postagger-2014-06-16/models/english-bidirectional-distsim.tagger',r'D:/stan/stanford-postagger-2014-06-16/stanford-postagger.jar')
import trialmult as p
#print (tag)

def tagging(line):
    words = word_tokenize(line)
    
    tagged = st.tag(words)
    #tagged=nltk.pos_tag(words)
    lemmatizer = WordNetLemmatizer();
    finalline=""
    
    for i in range(0,len(tagged)):
        if 'NN' in tagged[i][1]:
            finalline += lemmatizer.lemmatize(tagged[i][0],'n')+" "
        elif 'JJ' in tagged[i][1]:
            finalline += lemmatizer.lemmatize(tagged[i][0],'a')+" "
        elif 'RB' in tagged[i][1]:
            finalline += lemmatizer.lemmatize(tagged[i][0],'r')+" "
        elif 'VB' in tagged[i][1]:
            finalline += lemmatizer.lemmatize(tagged[i][0],'v')+" "
        else:
            finalline += lemmatizer.lemmatize(tagged[i][0])+" "
    return finalline


def remove_stopwords(line):
    stop_words = open("stopwordsnew.txt","r").read()
    words = word_tokenize(line)
    finalline=""
    
    for w in words:
        flag = 1
        for p in stop_words.split():
            if w == p:
                flag = 0
        if flag == 1:
            finalline += w+" "
    return finalline

def filter(line):   
    line = re.sub('RT\s *', ' ', line)                                              # remove re-tweets                                            
    line=line.lower()
    line = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', line)    # remove urls
    line = re.sub('pic.twitter.com\/[\w]*','',line)                                 # remove twitter pics links
    line = re.sub('stop loss','stoploss',line)
    line = con.expand_emoticons(line)
    line = re.sub('@[\w-]*:[\s] *', '', line)                                       # remove @userid          
    line = re.sub('\$[\w\.-]*[\s] *', '', line)                                     # remove cashtags '$'
    pattern=re.compile("[^\w'(\d\.\d)]")                                            # remove special chars
    line = pattern.sub(' ',line)
    
    line = con.expand_contractions(line)
    #print(line)
    #line = remove_stopwords(line)
    return line



##output= open("pos-out.txt","w")
out = open("tag-out_qwerty.txt","w")
    
for tweet in open('qwerty.txt'):
    tweet = filter(tweet)
    print("After filter: ",tweet)
    line = tagging(tweet)
    print("After pos tagging: ",line)
    sline = remove_stopwords(line)
    sline = n.negation(sline)
    print("After removal of sw and negation:",sline)
    print(p.sentiment(sline))
    out.write(sline+"\n")
    #output.write(tweet+"\n")

out.close()
#output.close()