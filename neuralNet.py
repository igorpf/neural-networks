#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 12/10/2017
import numpy as np
import functions as fn
from random import randint
class Layer():
    def __init__(self, neurons):
        self.neurons = neurons        

class Neuron():
    def __init__(self, inputs=[], activationFn=fn.sigmoid, output=None, error=None):
        """
            inputs->list of tuples containing the input (neuron or int) and its weight
                [(Neuron, 0.123)]
            activationFn -> function used to do the prediction (neuron output)
            output -> integer (used for neurons of the input layer)

          TODO: Bias input!  
        """
        self.inputs = inputs
        self.activationFn = activationFn
        self.output = output
        self.error = error
    #calculate output
    def predict(self):
        #sum each input*weight
        self.output = self.activationFn['fn'](
            reduce(lambda x,y: x+y, map(lambda x:x[0].output*(x[1]), self.inputs))
        )
        print self.output
        return self.output
    #def getOutput(self):
    #    return self.output



class NeuralNet():
    """docstring for neuralNet"""
    def __init__(self, neurons=[1], inputs=[1]): 
        """Constructor:
        args:
            neurons(list of ints):  list representing the size of each layer. The number
                of layers is the size of the list (of course)
        """               

        #Assert that len(inputs) == len(inputlayer)
        if neurons[0] != len(inputs):
            raise Exception('the inputs size must match the input layers size')
        inputLayer = Layer([Neuron(output=i) for i in inputs])
        layers = [inputLayer]
        for n in range(1,len(neurons)):
            layer = []            
            for x in range(neurons[n]):
                inputs = map(lambda x:(x, np.random.rand(), 0),layers[n-1].neurons)
                layer += [Neuron(inputs)]
            layers += [Layer(layer)]
        self.layers = layers

    def forwardProp(self):
        for n in range(1, len(self.layers)):
            for neuron in self.layers[n].neurons:
                neuron.predict()
            pass
        #return self.layers[-1].neurons[0].output

    def backProp(self, answers, alpha = 0.1, errorFn=fn.errorMeanSq):
        for i in range(len(self.layers[-1].neurons)):
            n =  self.layers[-1].neurons[n]
            n.error = n.output - answers[i]
        for l in range(1, len(self.layers) - 1):
            for i in range(len(self.layers[l].neurons)):
                n = self.layers[l].neurons[i]
                n.error = reduce(lambda x,y: x+y, map(lambda x:x.inputs[i][1]*x.error, self.layers[l+1].neurons)) * n.output * (1 - n.output)
        
        # computes derivatives (backpropagation and numerical)
        for l in range(1, len(self.layers)):
            for n in self.layers[l].neurons:
                for connection in n.inputs:
                    connection[2] = connection[0].output * n.error
                    #numericalDerivative = J...

        # update weights
        for l in range(1, len(self.layers)):
            for n in self.layers[l].neurons:
                for connection in n.inputs:
                    connection[1] = connection[1] - alpha * connection[2]

        # for n in xrange(1, len(self.layers), -1):
        #     for neuron in self.layers[n].neurons:
        #         neuron.predict()
        #     pass
        # return self.layers[-1].neurons[0].output
                
    def errorFunction:
        pass

if __name__ == '__main__':
    #print reduce(lambda x,y: x+y, map(lambda x:x[0]*x[1], [(1,2),(1,1)]))
    n = NeuralNet([2,2,3], [1,2])
    n.forwardProp()
    n.backProp([0.7,0.2,0.1])
    # l = [4,3,2]
    # print NeuralNet([1,2])
