import os
from gensim.models import Word2Vec
from nltk import word_tokenize
import glob


def readTags():
    with open('tags.txt') as f:
        tags = f.readline()
    tags = tags.split()
    return tags


fNames = readTags()


def tokenizeAll():
    words = []
    for name in fNames: # for each tag
        print('Tokenizing tag:', name)
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        allArticlesForTag = glob.glob(ROOT_DIR + '/texts/' + name + '/*.txt')
        for article in allArticlesForTag:
            with open(article) as f:  # open each article
                content = f.read()
                content = content.lower()

                wordTokenized = word_tokenize(content)  # wszystkie slowa z calego dokumentu
                words.append(wordTokenized)
    return words

def main():
    words = tokenizeAll()

    # train model
    model = Word2Vec(words, workers=4, min_count=1)

    # save model as a binary file and as a text file
    model.save('embeddings.bin')
    model.wv.save_word2vec_format('embeddings.txt', binary=False)


if __name__ == '__main__':
    main()