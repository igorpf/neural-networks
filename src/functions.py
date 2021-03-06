#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 18/10/2017
import numpy as np

#Activation functions
sigmoid = {
    'fn': lambda z: 1 / (1+np.exp(-z)),
    'der': lambda z: z*(1-z)
}

relu = {
    'fn': lambda z:z if z>0 else 0,
    'der': lambda z: 1 if z>0 else 0
}

#Error functions
errorMeanSq = {
    'fn': lambda out, ans: 0.5 * np.power(out-ans,2),
    'der': lambda out, ans: out - ans
}
