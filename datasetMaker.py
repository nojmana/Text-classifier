import numpy as np
from nltk import word_tokenize
from gensim.models import Word2Vec


def readTags():
    with open('tags.txt') as f:
        tags = f.readline()
    tags = tags.split()
    return tags


def postsToAveEmbeddings(post, embeddings):
    post = post.lower()
    mean_vec = [0 for _ in range(100)]
    wordTokenized = word_tokenize(post) # wszystkie slowa z calego dokumentu
    for token in wordTokenized:
        if token in embeddings:
            mean_vec += embeddings[token]
    mean_vec /= len(wordTokenized) # zawiera vector policzony tylko dla jednego dokumentu

    return mean_vec


def main():

    np.random.seed(0)
    fNames = readTags()
    numberLabels = {}
    for i in range(len(fNames)):
        numberLabels[fNames[i]] = i
    extension = '.txt'

    learnSet = open("learnset.csv", 'w')
    testSet = open("testset.csv", 'w')
    model = Word2Vec.load('embeddings.bin')

    for name in fNames:
        print('creating data set for tag:', name)
        with open('texts_cleaned/' + name + extension) as f:
            postVecs = []
            for line in f:
                postVecs.append(postsToAveEmbeddings(line, model))

            trainIndices = np.random.rand(
                len(postVecs)) < 0.7  # wylosuj 70% wierszy, które znajdą się w zbiorze treningowym
            train = [postVecs[i] for i in range(len(postVecs)) if
                     trainIndices[i] == 1]  # wybierz zbior treningowy (70%)
            test = [postVecs[i] for i in range(len(postVecs)) if
                    trainIndices[i] == 0]  # wybierz zbiór testowy (dopełnienie treningowego - 30%)

            for v in train:
                for x in v:
                    learnSet.write(str(x) + ',')
                learnSet.write(str(numberLabels[name]) + '\n')

            for v in test:
                for x in v:
                    testSet.write(str(x) + ',')
                testSet.write(str(numberLabels[name]) + '\n')

    learnSet.close()
    testSet.close()


if __name__ == '__main__':
    main()
