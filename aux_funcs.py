import pymongo
from math import sqrt

def euclidean(A, B):
    sumSq = 0.0

    # add up the squared differences
    for i in range(len(A)):
        sumSq += (A[i] - B[i]) ** 2

    # take the square root of the result
    return sqrt(sumSq)
