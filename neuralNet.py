#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 12/10/2017
import numpy as np

# Z na verdade é - sum(input*weight, 0 a n) - b (bias)
def sigmoid(z):
    return 1 / (1+np.exp(-z))

if __name__ == '__main__':
    print sigmoid(-10)