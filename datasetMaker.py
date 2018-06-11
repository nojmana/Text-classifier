import glob
import os

import numpy as np
from nltk import word_tokenize, re
from gensim.models import Word2Vec


def readTags():
    with open('tags.txt') as f:
        tags = f.readline()
    tags = tags.split()
    return tags


def postsToAveEmbeddings(post, embeddings, stopwords):
    post = post.lower()
    mean_vec = [0 for _ in range(100)]
    wordTokenized = word_tokenize(post)  # wszystkie slowa z calego dokumentu
    wordTokenizedLength = 0
    for token in wordTokenized:
        if token in stopwords:
            continue
        wordTokenizedLength += 1
        if token in embeddings:
            mean_vec += embeddings[token]
    mean_vec /= len(wordTokenized)  # zawiera vector policzony tylko dla jednego dokumentu

    return mean_vec


def main():
    from nltk.corpus import stopwords
    stopwords = set(stopwords.words('polish'))
    stopwords.update(['zgłoś', 'naruszenie', 'wczytuję', 'działam'])
    for i in range(100):
        stopwords.update(np.arange(0, 100))
    np.random.seed(0)
    fNames = readTags()
    numberLabels = {}
    for i in range(len(fNames)):
        numberLabels[fNames[i]] = i

    dataSet = open("dataSet.csv", 'w')
    model = Word2Vec.load('embeddings.bin')

    for name in fNames:
        print('creating data set for tag:', name)
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        allArticlesForTag = glob.glob(ROOT_DIR + '/texts/' + name + '/*.txt')
        for article in allArticlesForTag:
            with open(article) as f:
                text = ''
                for line in f:
                    if len(line) > 200:
                        text += line
                postVecs = []
                if len(text) > 0:
                    if len(text) > 2000:
                        texts = re.split('\s{4,}', text)
                        for i in texts:
                            if len(i) > 50:
                                postVecs.append(postsToAveEmbeddings(i, model, stopwords))
                    else:
                        postVecs.append(postsToAveEmbeddings(text, model, stopwords))

            for v in postVecs:
                for x in v:
                    dataSet.write(str(x) + ',')
                dataSet.write(str(numberLabels[name]) + '\n')

    dataSet.close()


if __name__ == '__main__':
    main()
