import sys
sys.path.append('../src')

from neuralNet import NeuralNet

if __name__ == '__main__':
    n = NeuralNet([3, 1, 2], "haberman")
    n.startTraining()