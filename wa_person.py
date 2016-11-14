import utils
import sys
import socket
import numpy as np

def generate_weights(num_of_attributes):
    """This function should generate a vector of size num_of_attributes
    that follow the rules of the game, i.e. all positive values should sum
    to 1, and there must be at least 1 positive value. Similarly, all negative
    values should sum to -1, and there should be at least 1 negative value
    
    The returned type should be a numpy array (np.array)"""

def adjust_weights(initial_weights, guess):
    """Adjust the initial weights provided within the rules stated in the game,
    i.e. no more than 5% of them can change, and those changed can't change by 
    more than 20%
    
    The returned type should be a numpy array (np.array)"""



def main():
    port = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', port))
    num_of_attributes = int(socket.recv(4))

    initial_weights = generate_weights(num_of_attributes)

    sock.sendall(utils.floats_to_msg2(initial_weights))
    # Send ideal (positive) candidate positions
    sock.sendall(utils.candidate_to_msg(initial_weights > 0))
    # Send anti-ideal (negative) candidate positions
    sock.sendall(utils.candidate_to_msg(initial_weights < 0))

    for i in range(20):
        matchmaker_guess = sock.recv(8 * num_of_attributes)
        matchmaker_guess = [float(attr.strip()) for attr in matchmaker_guess.split(',')]
        adjusted_weights = adjust_weights(initial_weights, matchmaker_guess)
        sock.sendall(utils.floats_to_msg2(adjusted_weights))

    sock.close()

if __name__=="__main__":
    main()
