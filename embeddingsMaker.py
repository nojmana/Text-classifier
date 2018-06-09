from gensim.models import Word2Vec
from nltk import word_tokenize


def readTags():
    with open('tags.txt') as f:
        tags = f.readline()
    tags = tags.split()
    return tags


fNames = readTags()
extension = '.txt'

def tokenizeAll():
    words = []
    for name in fNames:
        with open('texts_cleaned/' + name + extension) as f:
            content = f.read()
            content = content.lower()

            wordTokenized = word_tokenize(content) # wszystkie slowa z calego dokumentu
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