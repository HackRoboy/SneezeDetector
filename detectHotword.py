def get_distance(mfcc1, mfcc2):
    return 0.0


def get_avg_distance(mfcc1, mfccs):
    sum = 0.0
    n = 0
    for mfcc2 in mfccs:
        sum += get_distance(mfcc1, mfcc2)
        n += 1
    return sum/n

def get_avg_distance_between_all(mfccs):
    sum = 0.0
    n = 0
    for mfcc1 in mfccs:
        for mfcc2 in mfccs:
            sum += get_distance(mfcc1, mfcc2)
            n += 1
    return sum/n