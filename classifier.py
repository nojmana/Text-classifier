from datetime import datetime

import numpy as np
from sklearn.svm import SVC
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder


# random seed for reproducibility
seed = 0


# define baseline model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(40, input_dim=100, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def svcVersion(X, Y):
    classifier = SVC(kernel='linear', verbose=True)
    classifier.fit(X, Y)
    dataframe = pandas.read_csv("testset.csv", header=None)
    dataset = dataframe.values
    Xtest = dataset[:, 0:100].astype(float)
    Ytest = dataset[:, 100].astype(int)
    accuracy = classifier.score(Xtest, Ytest)

    print("W zbiorze testowym {n}% przypadków zostało poprawnie zaklasyfikowanych!".format(
        n=100. * accuracy))


def sequentialModelVersion(X, Y):
    # encode class values as integers
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_Y)
    estimator = KerasClassifier(build_fn=baseline_model, epochs=400, batch_size=10, verbose=0)
    kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
    results = cross_val_score(estimator, X, dummy_y, cv=kfold, verbose=1)
    print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))


def main():
    np.random.seed(seed)

    # load dataset
    dataframe = pandas.read_csv("learnset.csv", header=None)
    dataset = dataframe.values
    X = dataset[:, 0:100].astype(float)
    Y = dataset[:, 100]
    Y2 = dataset[:, 100].astype(int)

    print('Starting:' + str(datetime.now()))
    # sequentialModelVersion(X, Y)
    svcVersion(X, Y2) # acc = 44%
    print('Finished: ', str(datetime.now()))



if __name__ == '__main__':
    main()
