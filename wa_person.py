import utils
import sys
import socket
import numpy as np
import math
import random

def generate_weights(num_of_attributes):
    """This function should generate a vector of size num_of_attributes
    that follow the rules of the game, i.e. all positive values should sum
    to 1, and there must be at least 1 positive value. Similarly, all negative
    values should sum to -1, and there should be at least 1 negative value
    
    The returned type should be a numpy array (np.array)"""
    rands_pos = np.random.random(num_of_attributes / 2)
    rands_pos = rands_pos / sum(rands_pos) #normalize so they equal to 1
    rands_pos = [round(elem, 2) for elem in rands_pos]

    while(not(np.isclose(sum(rands_pos), 1.0))):
        #add little bits from the largest to the smallest until it's 1
        if sum(rands_pos) < 1.0:
            min_index = rands_pos.index(min(rands_pos))
            rands_pos[min_index] += 0.01
        else:
            max_index = rands_pos.index(max(rands_pos))
            rands_pos[max_index] -= 0.01

    rands_neg = np.random.random(num_of_attributes / 2)
    rands_neg = rands_neg / sum(rands_neg) #normalize so they equal to 1
    rands_neg = [round(elem, 2) for elem in rands_neg]

    while(not(np.isclose(sum(rands_neg), 1.0))):
        #add little bits from the largest to the smallest until it's 1
        if sum(rands_neg) < 1.0:
            min_index = rands_neg.index(min(rands_neg))
            rands_neg[min_index] += 0.01
        else:
            max_index = rands_neg.index(max(rands_neg))
            rands_neg[max_index] -= 0.01


    rands_neg = [-elem for elem in rands_neg]

    if num_of_attributes % 2 == 0:
        combined_arrays = np.hstack((rands_pos, rands_neg))
    else:
        combined_arrays = np.hstack((rands_pos, rands_neg, np.zeros(1)))

    np.random.shuffle(combined_arrays)

    return combined_arrays

def adjust_weights(initial_weights, guess):
    """Adjust the initial weights provided within the rules stated in the game,
    i.e. no more than 5% of them can change, and those changed can't change by 
    more than 20%
    
    The returned type should be a numpy array (np.array)"""
    # If true, we will shift positive numbers first
    shift_positive = np.random.random() >= 0.5
    num_to_change = math.floor(len(initial_weights) * .05)
    adjusted_weights = np.copy(initial_weights) #don't want to overwrite initial weights
    adjusted_weights = [elem for elem in adjusted_weights]

    if (num_to_change / 2 != 0):
        adjust_pair(adjusted_weights, shift_positive)
        shift_positive = not(shift_positive)
        num_to_change -=2

    adjusted_weights = np.array(adjusted_weights)
    return adjusted_weights

def adjust_pair(weights, adjust_positive):
    if adjust_positive:
        largest = max(elem for elem in weights)
        second_largest = max(elem for elem in weights if elem != largest)
        adjusted_amount = round(0.2 * second_largest, 4)
        # just in case rounding accidentally bumps us over the limit. i.e. if 
        # 0.2 * this weight is .009, and it rounds to .01, it would be illegal
        while adjusted_amount > (0.2 * second_largest):
            adjusted_amount -= 0.0001

        weights[weights.index(largest)] -= adjusted_amount
        weights[weights.index(second_largest)] += adjusted_amount

    else:
        smallest = min(elem for elem in weights)
        second_smallest = min(elem for elem in weights if elem != smallest)
        adjusted_amount = round(0.2 * second_smallest, 4)
        while abs(adjusted_amount) < abs(0.2 * second_smallest):
            adjusted_amount += 0.0001
        weights[weights.index(smallest)] += adjusted_amount
        weights[weights.index(second_smallest)] -= adjusted_amount

    weights = np.array(weights)
    return weights

#def adjust_triplet(weights, adjust_positive):
    #if adjust_positive:
    #    max_change = 0.2 * weights.index(max(weights)) 
    #    left_to_change = max_change
    #    smallest_pos_idx = min(elem for elem in weights if elem > 0)
    #    second_smallest_pos_idx = min(elem for elem in weights if elem > 0 and elem != weights[smallest_pos_idx])

    #    smallest_weight = weights[smallest_pos_idx]
    #    weights[smallest_pos_idx] += max(round(left_to_change / 2, 2), smallest_weight * 0.2)
        #This is not necessarily going to be valid. Consider left to change / 2 > valid shift
    #    left_to_change -= max(round(left_to_change / 2, 2), smallest_weight * 0.2)

    #    second_smallest = weights[

    #else:
    #    max_change = 0.2 * weights.index(min(weights))

    

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

#if __name__=="__main__":
#main()
