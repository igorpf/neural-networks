#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 12/10/2017
import numpy as np

class neuralNet():
    """docstring for neuralNet"""
    def __init__(self, neurons=[1]): 
        """Constructor:
        args:
            neurons(list of ints):  list representing the size of each layer. The number
                of layers is the size of the list (of course)
        """       
        #Don't forget to create bias neuron!!
        self.layers = [np.random.rand(1,n)[0] for n in neurons] #create a list of lists with random weights


"""
Possibility: 
    Net: 
        List<Layer>
            List<Neurons>
                List<Integer> weights 

"""
        


def sigmoid():
    """ Returns a dict containing the sigmoid function and its derivative

    Usage example: sigmoid()['fn'](10)
    """
    return {
        'fn': lambda z: 1 / (1+np.exp(-z)),
        'der': lambda z: z*(1-z)
    }

if __name__ == '__main__':
    print sigmoid()['fn'](-10)
    l = [4,3,2]
    print [np.random.rand(1,n)[0] for n in l]