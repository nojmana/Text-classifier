from datetime import datetime

import numpy as np
from sklearn.svm import SVC
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

# random seed for reproducibility
seed = 0


def svcVersion(x, y):
    msk = np.random.rand(len(x)) < 0.8
    x_train = x[msk]
    x_test = x[~msk]
    y_train = y[msk]
    y_test = y[~msk]
    classifier = SVC(kernel='linear', verbose=True)
    classifier.fit(x_train, y_train)
    accuracy = classifier.score(x_test, y_test)

    print("W zbiorze testowym {n}% przypadków zostało poprawnie zaklasyfikowanych!".format(
        n=100. * accuracy))


def sequentialModelVersion(x, y):
    y_binary = to_categorical(y)
    msk = np.random.rand(len(x)) < 0.8
    x_train = x[msk]
    x_test = x[~msk]
    y_train = y_binary[msk]
    y_test = y_binary[~msk]
    model = Sequential()
    model.add(Dense(500, input_dim=100, activation='relu'))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=500, batch_size=10, verbose=2)
    scores = model.evaluate(x_test, y_test)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


def main():
    np.random.seed(seed)

    # load dataset
    dataframe = pandas.read_csv("dataSet.csv", header=None)
    dataset = dataframe.values
    x = dataset[:, 0:100].astype(float)
    y = dataset[:, 100]
    y2 = dataset[:, 100].astype(int)

    print('Starting:' + str(datetime.now()))
    sequentialModelVersion(x, y) # 49,50 for 150 epochs
    # svcVersion(x, y2) # acc = 38,6%
    print('Finished: ', str(datetime.now()))


if __name__ == '__main__':
    main()
