#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These two lines are necessary to find source files!!!
import sys
sys.path.append('../src')

from neuralNet import NeuralNet, DataSet
from files import files

if __name__ == '__main__':
    f = files["haberman"]
    ds = DataSet(f)
    n = NeuralNet([3, 1, 2], ds.dataMatrix, numericalEvaluation=True)
    n.startTraining(1)