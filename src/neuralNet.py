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


    def getOutput(self):
        return self.output

    def setOutput(self, newOutput):
        self.output = newOutput


class NeuralNet():
    """docstring for neuralNet"""
    def __init__(self, neurons=[1], trainingSetName = "haberman"):
        """Constructor:
        args:
            neurons(list of ints):  list representing the size of each layer. The number
                of layers is the size of the list (of course)
        """

        self.trainingSetName = trainingSetName

        self.datasetMatrix = DataSet(files[trainingSetName]).dataMatrix

        if len(self.datasetMatrix[0]) - 1 != neurons[0]: #-1 because there are the attributes AND the class
            raise "DataSet values do not match the number of attributes of the input layer"

        #When train, add new values for the first layer's fake neurons
        inputLayer = Layer([Neuron(output=0) for i in range(neurons[0])])
        layers = [inputLayer]

        biasNeuronPrecessor = Neuron([])
        biasNeuronPrecessor.setOutput(1)
        biasNeuron = Neuron([biasNeuronPrecessor, 1, 0])
        biasNeuron.setOutput(1)
        for n in range(1, len(neurons)):
            layer = []
            for x in range(neurons[n]):
                inputs = map(lambda x:(x, np.random.rand(), 0), layers[n-1].neurons)
                inputs.insert(0, (biasNeuron, np.random.rand(), 0))
                layer += [Neuron(inputs)]
            layers += [Layer(layer)]
        self.layers = layers

    def startTraining(self):

        x = [[self.datasetMatrix[i % len(self.datasetMatrix)][j] for j in range(len(self.datasetMatrix[0]) - 1)] for i in range(len(self.datasetMatrix))]
        y = [[self.datasetMatrix[i % len(self.datasetMatrix)][-1]-1] for i in range(len(self.datasetMatrix))]

        for k in range(100):
            for i in range(len(y)):
                n.forwardProp(x[i % len(x)])
                n.backProp(x, y, i % len(x), 0.01)
                print i, n.errorFunction(x, y)
            print k, n.errorFunction(x, y)

    def forwardProp(self, instance, outputType = 0):
        for i in range(len(instance)):
            self.layers[0].neurons[i].output = instance[i]
            self.layers[0].neurons[i].testOutput = instance[i]
        for n in range(1, len(self.layers)):
            for neuron in self.layers[n].neurons:
                neuron.predict(outputType)
            pass

    def backProp(self, x, y, instanceIndex, alpha = 0.1, eps = np.finfo(np.float32).eps, errorFn=fn.errorMeanSq):

        # compute errors (deltas)
        for i in range(len(self.layers[-1].neurons)):
            n = self.layers[-1].neurons[i]
            n.error = n.output - y[instanceIndex][i]
        for l in reversed(range(1, len(self.layers) - 1)):
            for i in range(1, len(self.layers[l].neurons)): # does not calculate the delta for the first neuron because its the bias
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

            for k in range(len(y[i])):
                if self.layers[-1].neurons[k].testOutput != 0: #o que essa linha faz?
                    J = J + (-y[i][k] * (np.log(self.layers[-1].neurons[k].testOutput))
                                - (1 - y[i][k]) * (np.log(1 - self.layers[-1].neurons[k].testOutput)))

        return J / len(y)

    def cleanOutputs(self):
        for l in self.layers:
            for n in l.neurons:
                n.testOutput = n.output

class DataSet():
    def __init__(self, file):
        self.dataMatrix = []
        self.generateDataMatrix(file.fileName)
        self.normalizeFeatures(file.normRanges)

    def generateDataMatrix(self, file):
        with open(file) as file:
            for i, line in enumerate(file):
                line = line.rstrip("\n")
                words = map(lambda x: float(x) ,line.split(","))
                self.dataMatrix += [words]

    def normalizeFeatures(self, ranges = None):
        if ranges == None:
            self.ranges = self.defineRanges()
            print self.ranges
        else:
            self.ranges = ranges

        for i, row in enumerate(self.dataMatrix):
            for j, element in enumerate(self.dataMatrix[i]):
                bounds = self.ranges[j]
                if bounds == None:
                    continue
                self.dataMatrix[i][j] = (element-bounds[0])/(bounds[1]-bounds[0])

    def defineRanges(self):
        ranges = []
        for i in range(0, len(self.dataMatrix[0])):
            column = map(lambda x:x[i],self.dataMatrix)
            ranges += [[min(column),max(column)]]
        return ranges

if __name__ == '__main__':
    n = NeuralNet([3, 10, 10, 5, 1], "haberman")
    n.startTraining()

