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
        self.accuracy = np.zeros(self.numberOfClasses)
        self.fMeasure = np.zeros(self.numberOfClasses)

    def computeIteration(self, predicted, expected, expectedClass):
        expectedClassIndex = expectedClass# - 1
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

        print "Medium Precision: ", reduce(lambda x, y: x+y, self.precision)/self.numberOfClasses


    def computeRecall(self):

        for i in range(0, int(self.numberOfClasses)):
            recall = 0
            if self.truePositives[i] > 0:
                recall += self.truePositives[i]
                self.recall[i] = recall/(self.truePositives[i] + self.falseNegatives[i])

        print "Medium Recall: ", reduce(lambda x, y: x+y, self.recall)/self.numberOfClasses


    def computeAccuracy(self):

        for i in range(0, int(self.numberOfClasses)):
            accuracy = 0
            accuracy += self.truePositives[i] + self.trueNegatives[i]
            self.accuracy[i] = accuracy/(self.truePositives[i] + self.falsePositives[i] + self.trueNegatives[i] + self.falseNegatives[i])

        print "Medium Accuracy: ", reduce(lambda x, y: x+y, self.accuracy)/self.numberOfClasses


    def computeFMeasure(self, beta = 0.5):
        num = 0
        for i in range(0, int(self.numberOfClasses)):
            if self.precision[0] > 0 and self.recall[i] > 0:
                num = self.precision[i] * self.recall[i]
                den = beta**2 * self.precision[i] + self.recall[i]
            self.fMeasure[i] = (1 + beta**2) * (num/den)

        print "Medium F-Measure: ", reduce(lambda x, y: x+y, self.fMeasure)/self.numberOfClasses

    def resetConfusionMatrix(self):
        self.truePositives = np.zeros(self.numberOfClasses)
        self.falsePositives = np.zeros(self.numberOfClasses)
        self.trueNegatives = np.zeros(self.numberOfClasses)
        self.falseNegatives = np.zeros(self.numberOfClasses)
        self.precision = np.zeros(self.numberOfClasses)
        self.recall = np.zeros(self.numberOfClasses)
        self.accuracy = np.zeros(self.numberOfClasses)
        self.fMeasure = np.zeros(self.numberOfClasses)
