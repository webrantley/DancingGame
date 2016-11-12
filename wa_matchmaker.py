import utils
import sys
import socket
import numpy as np

def guess_weights(scores, weights):
    """Guess the weights of the Person's attributes based on past scores
    and weights of those scores, included as arguments. Return the your 
    guess as a numpy array (np.array)"""

def main():
    port = int(sys.argv[1])
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect(('localhost', port))
    num_of_attributes = int(socket.recv(4))

    scores = []
    weights = []
    # Get training data from architects
    for _ in range(20):
        training_sample = socket.recv(8 + 2 * num_of_attributes)
        score = float(training_sample[:7])
        scores.append(score)
        sample_weights = [float(attr.strip()) for attr in training_sample[8:].split(',')]
        weights.append(sample_weights)

    for _ in range(20):
        guess = guess_weights(scores, weights)
        socket.sendall(floats_to_msg4(guess))
        score = float(socket.recv(8))

        scores.append(score)
        weights.append(guess)

    socket.close()

if __name__=="__main__":
    main()
