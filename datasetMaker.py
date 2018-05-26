from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas
import numpy as np
from nltk import word_tokenize
from sklearn.metrics import classification_report
from gensim.models import Word2Vec

np.random.seed(0)

fNames = ['biznesC', 'filmC', 'literaturaC', 'motoryzacjaC', 'naukaC', 'politechnikaC', 'politykaC', 'sportC',
          'uniwersytetC', 'urodaC']
numberLabels = {'biznes':0, 'film':1, 'literatura':2, 'motoryzacja':3, 'nauka':4, 'politechnika':5, 'polityka':6,
                'sport':7, 'uniwersytet':8, 'uroda':9}

extension = '.txt'

learnSet = open("learnset.csv", 'w')
testSet = open("testset.csv", 'w')
model = Word2Vec.load('embeddings.bin')

def postsToAveEmbeddings(post, embeddings):
    post = post.lower()
    mean_vec = [0 for _ in range(100)]
    wordTokenized = word_tokenize(post) #wszystkie slowa z calego dokumentu
    for token in wordTokenized:
        if token in embeddings:
            mean_vec += embeddings[token]
    mean_vec /= len(wordTokenized) #zawiera vector policzony tylko dla jednego dokumentu

    return mean_vec

for name in fNames:
    with open(name + extension) as f:
        postVecs = []
        for line in f:
            postVecs.append(postsToAveEmbeddings(line, model))

        trainIndices = np.random.rand(len(postVecs)) < 0.7  # wylosuj 70% wierszy, które znajdą się w zbiorze treningowym
        train = [postVecs[i] for i in range(len(postVecs)) if trainIndices[i] == 1]  # wybierz zbior treningowy (70%)
        test = [postVecs[i] for i in range(len(postVecs)) if trainIndices[i] == 0]   # wybierz zbiór testowy (dopełnienie treningowego - 30%)

        for v in train:
            learnSet.write(str(v) + ';' + str(numberLabels[name[:-1]]) + '\n')

        for v in test:
            testSet.write(str(v) + '\n')




learnSet.close()
testSet.close()