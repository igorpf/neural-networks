import numpy as np


class PerformanceEvaluator:
    def __init__(self, numberOfClasses):
        self.numberOfClasses = numberOfClasses
        self.truePositives = np.zeros(self.numberOfClasses)
        self.falsePositives = np.zeros(self.numberOfClasses)
        self.trueNegatives = np.zeros(self.numberOfClasses)
        self.falseNegatives = np.zeros(self.numberOfClasses)
        self.precision = np.zeros(self.numberOfClasses)
        self.recall = np.zeros(self.numberOfClasses)
        self.f = np.zeros(self.numberOfClasses)

    def computeIteration(self, predicted, expected, expectedClass):
        expectedClassIndex = expectedClass - 1
        if predicted == 1 and expected == 1:
            self.truePositives[expectedClassIndex]+=1
        elif predicted == 1 and expected == 0:
            self.falsePositives[expectedClassIndex]+=1
        elif predicted == 0 and expected == 0:
            self.trueNegatives[expectedClassIndex]+=1
        elif predicted == 0 and expected == 1:
            self.falseNegatives[expectedClassIndex]+=1


    def computePrecision(self):

        for i in range(0, int(self.numberOfClasses)):
            precision = 0
            if self.truePositives[i] > 0:
                precision += self.truePositives[i]
                self.precision[i] = precision/(self.truePositives[i] + self.falsePositives[i])

        print "TP", self.truePositives
        print "FP", self.falsePositives
        print "TN", self.trueNegatives
        print "FN", self.falseNegatives

        print "Medium Precision: ", reduce(lambda x, y: x+y, self.precision)/self.numberOfClasses

    def resetConfusionMatrix(self):
        self.truePositives = np.zeros(self.numberOfClasses)
        self.falsePositives = np.zeros(self.numberOfClasses)
        self.trueNegatives = np.zeros(self.numberOfClasses)
        self.falseNegatives = np.zeros(self.numberOfClasses)
        self.precision = np.zeros(self.numberOfClasses)
        self.recall = np.zeros(self.numberOfClasses)
        self.f = np.zeros(self.numberOfClasses)
