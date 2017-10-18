#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 12/10/2017
import numpy as np

#A dict containing the sigmoid function and its derivative
sigmoid = {
    'fn': lambda z: 1 / (1+np.exp(-z)),
    'der': lambda z: z*(1-z)
}

linear = {
    'fn': lambda z: z,
    'der': lambda z: 1
}

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
                inputs = map(lambda x:(x, np.random.rand() ),layers[n-1].neurons)
                layer += [Neuron(inputs)]
            layers += [Layer(layer)]
        self.layers = layers

    def train(self):
        for n in range(1, len(self.layers)):
            for neuron in self.layers[n].neurons:
                neuron.predict()
            pass
        return self.layers[-1].neurons[0].getOutput()

class Layer():
    def __init__(self, neurons):
        self.neurons = neurons        

class Neuron():
    def __init__(self, inputs=[], activationFn=sigmoid, output=None):
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
    #calculate output
    def predict(self):
        self.output = self.activationFn['fn'](
            reduce(lambda x,y: x+y, map(lambda x:x[0].getOutput()*x[1], self.inputs))
        )
        print self.output
        return self.output
    def getOutput(self):
        return self.output

if __name__ == '__main__':
    #print reduce(lambda x,y: x+y, map(lambda x:x[0]*x[1], [(1,2),(1,1)]))
    n = NeuralNet([2,2,3], [1,2])
    print n.train()
    # l = [4,3,2]
    # print NeuralNet([1,2])