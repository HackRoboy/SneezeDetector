import numpy as np
from fastdtw import fastdtw
from dtw import dtw
from scipy.spatial.distance import euclidean


def get_distance(mfcc1, mfcc2):
    dist, cost, accCost, path = dtw(mfcc1, mfcc2, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
    return dist


def get_avg_distance(mfcc1, mfccs):
    sum = 0.0
    n = 0
    for mfcc2 in mfccs:
        sum += get_distance(mfcc1, mfcc2)
        n += 1
    return sum / n


def get_avg_distance_between_all(mfccs):
    sum = 0.0
    n = 0
    for mfcc1 in mfccs:
        for mfcc2 in mfccs:
            sum += get_distance(mfcc1, mfcc2)
            n += 1
    return sum / n
