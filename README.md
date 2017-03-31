# Dating Game

AI built to compete in a class competition. More details [here](http://cs.nyu.edu/courses/fall16/CSCI-GA.2965-001/dating.html)

# Strategy

When guessing the weights, we perform linear regression and ridge regression, and guess based on the closest fit. Our model is updated after every guess.

When generating the weights, we found that having a random distribution of weights to be best. High weights allow the opponent to quickly guess our weights, so we keep them roughly the same, with some small variation.
