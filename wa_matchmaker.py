import utils
import sys
import socket
import numpy as np
from sklearn import datasets, linear_model

def guess_weights(scores, weights, iter_num):
    X = np.array([np.array(weight) for weight in weights])
    y = np.array(scores)
    if(iter_num % 2 == 0):
        clf = linear_model.Ridge(alpha=0.1)
    else:
        clf = linear_model.LinearRegression()
    clf.fit(X, y)
    a = clf.coef_
    for x in np.nditer(a, op_flags=['readwrite']):
        if x < 0:
            x[...] = 0
        else:
            x[...] = 1
    return a
    """Guess the weights of the Person's attributes based on past scores
    and weights of those scores, included as arguments. Return the your 
    guess as a numpy array (np.array)"""

def main():
    port = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', port))
    num_of_attributes = int(sock.recv(4))

    scores = []
    weights = []
    # Get training data from architects
    for _ in range(20):
        training_sample = sock.recv(8 + 2 * num_of_attributes)
        score = float(training_sample[:7])
        scores.append(score)
        sample_weights = [float(attr.strip()) for attr in training_sample[8:].split(',')]
        weights.append(sample_weights)

    for i in range(20):
        guess = guess_weights(scores, weights, i)
        sock.sendall(utils.floats_to_msg4(guess))
        score = float(sock.recv(8))
        scores.append(score)
        weights.append(guess)

    sock.close()

if __name__=="__main__":
    main()
