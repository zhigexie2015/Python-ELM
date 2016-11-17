#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extreme Learning Machine
This script is ELM for binary and multiclass classification.
"""

import numpy as np

from sklearn import preprocessing
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.datasets import fetch_mldata
from sklearn import cross_validation
from sklearn.datasets import load_svmlight_file


class ELM (BaseEstimator, ClassifierMixin):

    """
    3 step model ELM
    """

    def __init__(self,
                 hid_num,
                 a=1):
        """
        Args:
        hid_num (int): number of hidden neurons
        a (int) : const value of sigmoid funcion
        """
        self.hid_num = hid_num
        self.a = a

    def __sigmoid(self, x):
        """
        sigmoid function
        Args:
        x ([[float]]) array : input

        Returns:
        float: output of sigmoid
        """
        return 1 / (1 + np.exp(-self.a * x))

    def __add_bias(self, X):
        """add bias to list

        Args:
        x_vs [[float]] Array: vec to add bias

        Returns:
        [float]: added vec

        Examples:
        >>> e = ELM(10, 3)
        >>> e._ELM__add_bias(np.array([[1,2,3], [1,2,3]]))
        array([[ 1.,  2.,  3.,  1.],
               [ 1.,  2.,  3.,  1.]])
        """

        return np.c_[X, np.ones(X.shape[0])]

    def __ltov(self, n, label):
        """
        trasform label scalar to vector
        Args:
        n (int) : number of class, number of out layer neuron
        label (int) : label

        Exmples:
        >>> e = ELM(10, 3)
        >>> e._ELM__ltov(3, 1)
        [1, -1, -1]
        >>> e._ELM__ltov(3, 2)
        [-1, 1, -1]
        >>> e._ELM__ltov(3, 3)
        [-1, -1, 1]
        """
        return [-1 if i != label else 1 for i in range(1, n + 1)]

    def fit(self, X, y):
        """
        learning

        Args:
        X [[float]] array : feature vectors of learnig data
        y [[float]] array : labels of leanig data
        """
        # number of class, number of output neuron
        self.out_num = max(y)

        if self.out_num != 1:
            y = np.array([self.__ltov(self.out_num, _y) for _y in y])

        # add bias to feature vectors
        X = self.__add_bias(X)

        # generate weights between input layer and hidden layer
        np.random.seed()
        self.W = np.random.uniform(-1., 1.,
                                   (self.hid_num, X.shape[1]))

        # find inverse weight matrix
        _H = np.linalg.pinv(self.__sigmoid(np.dot(self.W, X.T)))

        self.beta = np.dot(_H.T, y)

        return self

    def predict(self, X):
        """
        predict classify result

        Args:
        X [[float]] array: feature vectors of learnig data

        Returns:
        [int]: labels of classification result
        """

        _H = self.__sigmoid(np.dot(self.W, self.__add_bias(X).T))
        y = np.dot(_H.T, self.beta)

        if self.out_num == 1:
            return np.sign(y)
        else:
            return np.argmax(y, 1) + np.ones(y.shape[0])


def main():

    db_names = ['australian', 'iris']

    hid_nums = [10, 20, 30]

    for db_name in db_names:
        print(db_name)
        data_set = fetch_mldata(db_name)
        data_set.data = preprocessing.scale(data_set.data)

        for hid_num in hid_nums:
            print(hid_num, end=' ')
            e = ELM(hid_num)
            ave = 0
            for i in range(10):
                scores = cross_validation.cross_val_score(
                    e, data_set.data, data_set.target, cv=5, scoring='accuracy')
                ave += scores.mean()
            ave /= 10
            print("Accuracy: %0.3f " % (ave))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()