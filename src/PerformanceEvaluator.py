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
            precision+=self.truePositives[i]
            precision+=self.trueNegatives[i]
            n = self.truePositives[i] + self.trueNegatives[i] + self.falsePositives[i] + self.falseNegatives[i]
            self.precision[i] = precision/n
        print "Medium Precision: ", reduce(lambda x,y: x+y, self.precision)/len(self.precision)

    def resetConfusionMatrix(self):
        self.truePositives = np.zeros(self.numberOfClasses)
        self.falsePositives = np.zeros(self.numberOfClasses)
        self.trueNegatives = np.zeros(self.numberOfClasses)
        self.falseNegatives = np.zeros(self.numberOfClasses)
        self.precision = np.zeros(self.numberOfClasses)
        self.recall = np.zeros(self.numberOfClasses)
        self.f = np.zeros(self.numberOfClasses)
