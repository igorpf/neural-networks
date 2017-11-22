#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by igor on 12/10/2017
import numpy as np
import functions as fn
from files import files
import crossValidation as cv
from PerformanceEvaluator import PerformanceEvaluator

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
        self.testOutput = newOutput


class NeuralNet():
    """docstring for neuralNet"""
    def __init__(self, neurons=[1], trainingSetName = "haberman"):
        """Constructor:
        args:
            neurons(list of ints):  list representing the size of each layer. The number
                of layers is the size of the list (of course)
        """

        self.trainingSetName = trainingSetName
        self.regularizationRate = 1

        self.datasetMatrix = DataSet(files[trainingSetName]).dataMatrix

        self.attributesList = [[self.datasetMatrix[i % len(self.datasetMatrix)][j] for j in range(len(self.datasetMatrix[0]) - 1)] for i in range(len(self.datasetMatrix))]
        if len(self.attributesList[0]) != neurons[0]: #-1 because there are the attributes AND the class
            raise "DataSet values do not match the number of attributes of the input layer"

        self.expectedClassList = [self.datasetMatrix[i % len(self.datasetMatrix)][-1] for i in range(len(self.datasetMatrix))]
        self.possibleClasses = max(self.expectedClassList)

        if self.possibleClasses != neurons[-1]:
            raise "Number of output neurons does not match with the number of classes of given DataSet."

        self.performanceEvaluator = PerformanceEvaluator(self.possibleClasses)

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

        x = self.attributesList
        y = []

        for i in range(len(self.expectedClassList)):
            expectedOutputsForLastLayer = []
            for possibleClass in range(1, int(self.possibleClasses) + 1):
                expectedOutputsForLastLayer.append(1 if possibleClass == self.expectedClassList[i] else 0)
            y.append(expectedOutputsForLastLayer)
        print y

        for k in range(10):
            for i in range(len(y)):
                n.forwardProp(x[i])
                n.backProp(x, y, i, 0.1)
            print k, n.errorFunction(x, y)
            self.performanceEvaluator.computePrecision()

    def forwardProp(self, instance, outputType = 0):
        for i in range(len(instance)):
            self.layers[0].neurons[i].output = instance[i]
            self.layers[0].neurons[i].testOutput = instance[i]
        for n in range(1, len(self.layers)):
            for neuron in self.layers[n].neurons:
                neuron.predict(outputType)
            pass

    def backProp(self, x, y, instanceIndex, alpha=0.003, numericalEval=False, eps=np.finfo(np.float32).eps, errorFn=fn.errorMeanSq):

        #print "\n"

        highestOutputValue = 0
        highestOutputValueClass = -1
        # compute errors (deltas)
        for i in range(len(self.layers[-1].neurons)):
            n = self.layers[-1].neurons[i]
            n.error = n.output - y[instanceIndex][i]
            if n.output > highestOutputValue:
                highestOutputValue = n.output
                highestOutputValueClass = i + 1 #+ 1 pois as classes começam em 1

         for i in range(len(self.layers[-1].neurons)):
             n = self.layers[-1].neurons[i]
             iNeuronOutput = 0 if n.output < 0.5 else 1
             self.performanceEvaluator.computeIteration(iNeuronOutput, y[instanceIndex][i], highestOutputValueClass)

        #print "saída da rede:", highestOutputValueClass, "saída esperada:", self.expectedClassList[instanceIndex]

        for l in reversed(range(1, len(self.layers) - 1)):
            for i in range(len(self.layers[l].neurons)):
                n = self.layers[l].neurons[i]
                n.error = reduce(lambda x,y: x+y, map(lambda x:x.inputs[i+1][1]*x.error, self.layers[l+1].neurons)) * n.output * (1 - n.output)

        # computes derivatives (gradients) - backpropagation and numerical
        for l in range(1, len(self.layers)):
            neuron = 0
            for n in self.layers[l].neurons:
                neuron = neuron + 1
                for c in range(len(n.inputs)):
                    # print map(lambda x:x[1]**2, n.inputs[1:])
                    reg = self.regularizationRate * n.inputs[c][1]
                    # print reg
                    n.inputs[c] = (n.inputs[c][0], n.inputs[c][1], n.inputs[c][0].output * n.error+reg)
                    if numericalEval:
                        self.numericalEvaluation(c, eps, instanceIndex, l, n, neuron, x, y)

        # update weights
        for l in range(1, len(self.layers)):
            for n in self.layers[l].neurons:
                for c in range(len(n.inputs)):                    
                    n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] - alpha * n.inputs[c][2], n.inputs[c][2])

    def numericalEvaluation(self, c, eps, instanceIndex, l, n, neuron, x, y):
        print "\nGradients for input", c, "weight of neuron", neuron, "of layer", l
        print "Backpropagation derivative: ", n.inputs[c][2]
        n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] + eps, n.inputs[c][2])
        error1 = self.errorFunction(x, y, instanceIndex)
        n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] - eps, n.inputs[c][2])
        n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] - eps, n.inputs[c][2])
        error2 = self.errorFunction(x, y, instanceIndex)
        n.inputs[c] = (n.inputs[c][0], n.inputs[c][1] + eps, n.inputs[c][2])
        numericalDerivative = (error1 - error2) / (2 * eps)
        print "Numerical derivative: ", numericalDerivative

    def errorFunction(self, x, y, instanceIndex = None):
        self.cleanOutputs()

        J = 0
        for i in range(len(y)):
            if instanceIndex != None:
                i = instanceIndex
            self.forwardProp(x[i], 1)

            for k in range(len(y[i])):
                output = self.layers[-1].neurons[k].testOutput
                if output == 0:
                    output = 0.0000001
                if output == 1:
                    output = 0.9999999
                J = J - y[i][k] * (np.log(output)) - (1 - y[i][k]) * (np.log(1 - output))
        allInputs = []
        for n in map(lambda x:x.neurons,self.layers):
            for i in n:
                allInputs.append(i.inputs)
        # flatten a list of lists to a one-level list
        allInputs = map(lambda x:x[1]**2,[i for sub in allInputs for i in sub])
        reg = self.regularizationRate* reduce(lambda x,y: x+y,allInputs)/(2*len(y))
        # print reg
        J += reg
        

        return J / len(y)

    def cleanOutputs(self):
        for l in self.layers:
            for n in l.neurons:
                n.testOutput = n.output

    def debug(self):
        print "\n\n\n----------------------------------------------------"
        for l in range(1, len(self.layers)):
            neuronNumber = 0
            print "\n\nLayer ", l
            for neuron in self.layers[l].neurons:
                neuronNumber = neuronNumber + 1
                print "\n Neuron ", neuronNumber, "Activation: ", neuron.output
                for c in range(len(neuron.inputs)):
                    print "\t\tActivation: ", neuron.inputs[c][0].output, "\tWeight: ", neuron.inputs[c][1]

class DataSet():
    def __init__(self, file):
        self.dataMatrix = []
        self.generateDataMatrix(file.fileName)
        self.normalizeFeatures(file.normRanges)

    def generateDataMatrix(self, file):
        with open(file) as file:
            for i, line in enumerate(file):
                line = line.rstrip("\n")
                words = map(lambda x: float(x), line.split(","))
                self.dataMatrix += [words]

    def normalizeFeatures(self, ranges=None):
        if ranges==None:
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
    n = NeuralNet([3, 10, 10, 2], "haberman")
    n.startTraining()
