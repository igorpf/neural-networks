#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 15/11/2017

# These two lines are necessary to find source files!!!
import sys
sys.path.append('../src')

import crossValidation as cv
from neuralNet import NeuralNet, DataSet
from files import files

def testFold(file):
    f = files[file]
    ds = DataSet(f)
    folds = cv.fold(ds.dataMatrix, f.classProportion)
    print "Folds' size should be 5 and is: {0}".format(len(folds)) 
    for i, fold in enumerate(folds):
        print "Fold {}, size {}".format(i,len(fold))
        for j,clazz in enumerate(f.classes):
            # print fold, clazz
            print "Class {}, proportion should be {} and is {}".format(clazz, f.classProportion[j],getFoldProportion(fold, clazz))


def getFoldProportion(fold, clazz):
    return len(filter(lambda x: x[-1]== clazz, fold))/ float(len(fold))
if __name__ == '__main__':
    testFold('haberman')
    # testFold('wine')