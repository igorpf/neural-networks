#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 12/10/2017
import numpy as np
import functions as fn
import cPickle as pickle

class Layer():
    def __init__(self, neurons):
        self.neurons = neurons        

class Neuron():
    def __init__(self, inputs=[], activationFn=fn.sigmoid, output=None):
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
        #sum each input*weight
        self.output = self.activationFn['fn'](
            reduce(lambda x,y: x+y, map(lambda x:x[0].getOutput()*x[1], self.inputs))
        )
        print self.output
        return self.output
    def getOutput(self):
        return self.output



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

    def saveNet(self):
        with open("./save/neuralNet.txt", "wb") as output:
            pickle.dump(self.layers, output, pickle.HIGHEST_PROTOCOL)

    def forwardProp(self):
        for n in range(1, len(self.layers)):
            for neuron in self.layers[n].neurons:
                neuron.predict()
            pass
        return self.layers[-1].neurons[0].getOutput()

    def backProp(self, answer, errorFn=fn.errorMeanSq):
        pass
        # for n in xrange(1, len(self.layers), -1):
        #     for neuron in self.layers[n].neurons:
        #         neuron.predict()
        #     pass
        # return self.layers[-1].neurons[0].getOutput()


class DataSet():
    def __init__(self, file):
        self.dataMatrix = []
        self.generateDataMatrix(file)

    def generateDataMatrix(self, file):
        with open(file) as file:
            for i, line in enumerate(file):
                line = line.rstrip("\n")
                words = line.split(",")
                self.dataMatrix += [words]
                print self.dataMatrix

if __name__ == '__main__':
    #print reduce(lambda x,y: x+y, map(lambda x:x[0]*x[1], [(1,2),(1,1)]))
    n = NeuralNet([2,2,3], [1,2])
    print n.forwardProp()
    # l = [4,3,2]
    # print NeuralNet([1,2])
    ds = DataSet("./datasets/habermandata.txt")
    n.saveNet()
