import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
    
short_p = open("Final/tag-out_fpos.txt","r").read()
short_n = open("Final/tag-out_fneg.txt","r").read()
short_nu = open("Final/tag-out_test.txt","r").read()
short_pos = short_p.lower()
short_neg = short_n.lower()
short_neu = short_nu.lower()
documents = []
all_words = []

allowed_word_types = ["V"]


for p in short_pos.split('\n'):
    documents.append( (p, "pos") )
    words = word_tokenize(p)

    for w in words:
            all_words.append(w.lower())
    
for p in short_neg.split('\n'):
    documents.append( (p, "neg") )
    words = word_tokenize(p)
    for w in words:
            all_words.append(w.lower())
    
for p in short_neu.split('\n'):
    documents.append( (p, "neu") )
    words = word_tokenize(p)
    for w in words:
            all_words.append(w.lower())

wf_f = open("featuresff.pickle","rb")
word_features = pickle.load(wf_f)
wf_f.close()
print(len(word_features))

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

print("Featureset started")

featuresets = [(find_features(rev), category) for (rev, category) in documents]

print(len(documents))
random.shuffle(featuresets)
print("Featureset loaded")

testing_set = featuresets[1400:]
training_set = featuresets[:1400]

wf_f = open("Final/LinearSVC_classifier5k.pickle","rb")
LinearSVC_classifier = pickle.load(wf_f)
wf_f.close()
wf_f = open("Final/NuSVC_classifier5k.pickle","rb")
NuSVC_classifier = pickle.load(wf_f)
wf_f.close()
wf_f = open("Final/classifier5k.pickle","rb")
classifier = pickle.load(wf_f)
wf_f.close()
voted_classifier = VoteClassifier(
                                  classifier,
                                  LinearSVC_classifier,
                                  NuSVC_classifier
                                 )
def sentiment(text):
    feats = find_features(text)

    return voted_classifier.classify(feats)