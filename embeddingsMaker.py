from gensim.models import Word2Vec
from nltk import word_tokenize

fNames = ['biznesC', 'filmC', 'literaturaC', 'motoryzacjaC', 'naukaC', 'politechnikaC', 'politykaC', 'sportC',
          'uniwersytetC', 'urodaC']
extension = '.txt'

def tokenizeAll():
    words = []
    for name in fNames:
        with open(name + extension) as f:
            content = f.read()
            content = content.lower()

            wordTokenized = word_tokenize(content) #wszystkie slowa z calego dokumentu
            words.append(wordTokenized)

    return words

words = tokenizeAll()

print("Tokenized")

# train model
model = Word2Vec(words, workers=4, min_count=1)

print("Model created")
# save model
model.save('embeddings.bin')
model.wv.save_word2vec_format('embeddings.txt', binary=False)
# load model
new_model = Word2Vec.load('embeddings.bin')
print(new_model)