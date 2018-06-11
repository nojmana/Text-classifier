import glob
import os
import nltk


def mostCommonWords(text, stopwords):
    wordDictionary = {}

    for word in text:
        if word not in stopwords and len(word) > 1:
            wordDictionary[word] = wordDictionary.get(word, 0) + 1

    mostCommonWords = []
    i = 0
    for mostCommon in sorted(wordDictionary, key=wordDictionary.get, reverse=True):
        mostCommonWords.append(mostCommon)
        print(wordDictionary[mostCommon], mostCommon)
        i += 1
        if i == 100:
            return mostCommonWords


def countMostCommonWords():
    from nltk.corpus import stopwords
    file = open('analysis.txt', 'a')
    stopwords = set(stopwords.words('polish'))
    stopwords.update(['zgłoś', 'naruszenie', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    fNames = readTags()
    for fName in fNames:
        print("\nTag:", fName)
        content = ''
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        allArticlesForTag = glob.glob(ROOT_DIR + '/texts/' + fName + '/*.txt')
        for article in allArticlesForTag:
            with open(article) as f:
                content += f.read()
        content = content.lower()
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        content = tokenizer.tokenize(content)
        mostCommon = mostCommonWords(content, stopwords)
        file.write(fName + ': ')
        for word in mostCommon:
            file.write(word + ' ')
        file.write('\n')


def readTags():
    with open('tags.txt') as f:
        tags = f.readline()
    tags = tags.split()
    return tags


countMostCommonWords()



