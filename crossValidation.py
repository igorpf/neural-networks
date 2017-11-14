#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 13/11/2017

# k-folding

# proportions -> list of proportion of each class ([0,1])
# classIndex -> which position is the class predicted? default: last
def fold(matrix, proportions, classIndex=-1,k=5):
	size = len(matrix)/k
	groups = {}
	for i, row in enumerate(matrix):
		key = row[classIndex]
		groups[key] = groups.get(key, []) + [row]
	return groups