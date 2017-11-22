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
            if self.truePositives[i] > 0:
                accuracy += self.truePositives[i] + self.trueNegatives[i]
                self.accuracy[i] = accuracy/(self.truePositives[i] + self.falsePositives[i] + self.trueNegatives + self.falseNegatives[i])

        print "Medium Accuracy: ", reduce(lambda x, y: x+y, self.accuracy)/self.numberOfClasses


    def resetConfusionMatrix(self):
        self.truePositives = np.zeros(self.numberOfClasses)
        self.falsePositives = np.zeros(self.numberOfClasses)
        self.trueNegatives = np.zeros(self.numberOfClasses)
        self.falseNegatives = np.zeros(self.numberOfClasses)
        self.precision = np.zeros(self.numberOfClasses)
        self.recall = np.zeros(self.numberOfClasses)
        self.accuracy = np.zeros(self.numberOfClasses)
        self.f = np.zeros(self.numberOfClasses)
