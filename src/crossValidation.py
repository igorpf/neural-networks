#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 13/11/2017
from random import shuffle
# k-folding

# proportions -> list of proportion of each class ([0,1])
# classIndex -> which position is the class predicted? default: last
def fold(matrix, proportions, classIndex=-1,k=5):    
    groups = {}
    for i, row in enumerate(matrix):
        key = row[classIndex]
        groups[key] = groups.get(key, []) + [row]
    #randomness is introduced here to simplify the algorithm
    for key in groups:
        shuffle(groups[key])

    size = len(matrix)/k
    folds = []
    
    for iteration in range(k):    
        fold = []       
        for i,prop in enumerate(proportions):
            s = int(prop * size)
            key = float(i+1)
            fold += groups[key][:s]
            groups[key] = groups[key][s:]
        folds+= [fold]
    #Some elements may be left after this procedure, so we want to distribute them equally to the folds
    anyElementsLeft = True
    nextFold = 0
    while anyElementsLeft:
        anyElementsLeft = False
        for key in groups:
            if len(groups[key]) == 0:
                continue
            anyElementsLeft = True
            folds[nextFold].append(groups[key].pop()) 
            nextFold = (nextFold+1) % k
    return folds