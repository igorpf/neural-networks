#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 12/10/2017
import numpy as np
import functions as fn
from random import randint
import cPickle as pickle
from files import files
import crossValidation as cv

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
        self.testOutput = 0
        self.error = 0
    #calculate output
    def predict(self, outputType = 0):
        #sum each input*weight
        if(outputType == 0):
            self.output = self.activationFn['fn'](
                reduce(lambda x,y: x+y, map(lambda x:x[0].output*(x[1]), self.inputs))
            )
        else:
            self.testOutput = self.activationFn['fn'](
                reduce(lambda x,y: x+y, map(lambda x:x[0].testOutput*(x[1]), self.inputs))
            )
        #print self.testOutput


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

    def saveNet(self):
        with open("./save/neuralNet.txt", "wb") as output:
            pickle.dump(self.layers, output, pickle.HIGHEST_PROTOCOL)

    def forwardProp(self):
    def forwardProp(self, instance, outputType = 0):
        for i in range(len(instance)):
            self.layers[0].neurons[i].output = instance[i]
            self.layers[0].neurons[i].testOutput = instance[i]
        for n in range(1, len(self.layers)):
            for neuron in self.layers[n].neurons:
                neuron.predict(outputType)
            pass

    def backProp(self, x, y, instanceIndex, alpha = 0.1, eps = np.finfo(np.float32).eps, errorFn=fn.errorMeanSq):
        n = 0

        # compute errors (deltas)
        for i in range(len(self.layers[-1].neurons)):
            n = self.layers[-1].neurons[i]
            n.error = n.output - y[instanceIndex][i]
        for l in reversed(range(1, len(self.layers) - 1)):
            for i in range(len(self.layers[l].neurons)):
                n = self.layers[l].neurons[i]
                n.error = reduce(lambda x,y: x+y, map(lambda x:x.inputs[i][1]*x.error, self.layers[l+1].neurons)) * n.output * (1 - n.output)

        # computes derivatives (gradients) - backpropagation and numerical
        for l in range(1, len(self.layers)):
            neuron = 0
            for n in self.layers[l].neurons:
                neuron = neuron + 1
                for c in range(len(n.inputs)):
                    n.inputs[c] = (n.inputs[c][0], n.inputs[c][1], n.inputs[c][0].output * n.error)
                    """print "\nGradients for input", c, "weight of neuron", neuron, "of layer", l
                    print "Backpropagation derivative: ", n.inputs[c][2]

                    n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] + eps, n.inputs[c][2])
                    error1 = self.errorFunction(x, y, instanceIndex)
                    n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] - eps, n.inputs[c][2])

                    n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] - eps, n.inputs[c][2])
                    error2 = self.errorFunction(x, y, instanceIndex)
                    n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] + eps, n.inputs[c][2])

                    numericalDerivative = (error2 - error1) / (2 * eps)
                    print "Numerical derivative: ", numericalDerivative"""

        # update weights
        for l in range(1, len(self.layers)):
            for n in self.layers[l].neurons:
                for c in range(len(n.inputs)):
                    n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] - alpha * n.inputs[c][2], n.inputs[c][2])

    def errorFunction(self, x, y, instanceIndex = None):
        self.cleanOutputs()

        J = 0
        for i in range(len(y)):
            if instanceIndex != None:
                i = instanceIndex
            self.forwardProp(x[i], 1)
            aux = 0
            for k in range(len(y[i])):
                J = J + (-y[i][k] * (-np.log(self.layers[-1].neurons[k].testOutput))
                                - (1 - y[i][k]) * (-np.log(1 - self.layers[-1].neurons[k].testOutput)))
                aux = aux + (-y[i][k] * (-np.log(self.layers[-1].neurons[k].testOutput)) - (1 - y[i][k]) * (-np.log(1 - self.layers[-1].neurons[k].testOutput)))

        return J / len(y)

    def cleanOutputs(self):
        for l in self.layers:
            for n in l.neurons:
                n.testOutput = n.output



class DataSet():
    def __init__(self, file):
        self.dataMatrix = []
        self.generateDataMatrix(file)

    def generateDataMatrix(self, fileObj):
        with open(fileObj.fileName) as file:
            for i, line in enumerate(file):
                line = line.rstrip("\n")
                words = map(lambda x: float(x) ,line.split(","))
                self.dataMatrix += [words]
            #the ranges for normalization can be passed as arguments for optimization
            if fileObj.normRanges==None:
                self.ranges = []
                for i in range(0, len(self.dataMatrix[0])):
                    column = map(lambda x:x[i],self.dataMatrix)
                    self.ranges += [[min(column),max(column)]]
                print self.ranges
            else:
                self.ranges = fileObj.normRanges
            #feature normalization
            for i, row in enumerate(self.dataMatrix):
                for j, element in enumerate(self.dataMatrix[i]):
                    bounds = self.ranges[j]
                    if bounds == None:
                        continue
                    self.dataMatrix[i][j] = (element-bounds[0])/(bounds[1]-bounds[0])
if __name__ == '__main__':
    #print reduce(lambda x,y: x+y, map(lambda x:x[0]*x[1], [(1,2),(1,1)]))
    x = [[1,2,1],[2,3,1],[0.5,1,1.5]]
    y = [[0.3,0.8],[0.7,0.2],[0.3,0.2]]
    n = NeuralNet([3,2,5,10,2], x[0])
    for i in range(500):
        n.forwardProp(x[i % len(x)])
        n.backProp(x, y, i % len(x), 0.1)
        print n.errorFunction(x, y)


    n = NeuralNet([2,2,3], [1,2])
    print n.forwardProp()
    h = files['haberman']
    ds = DataSet(h)
