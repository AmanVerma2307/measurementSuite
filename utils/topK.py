import numpy as np

def selectTopK(eerVec,
               scoreVec):

    """
    Function to return topK EER values score values

    INPUTS:-
    1) eerVec: Input EER values
    2) scoreVec: Score values

    Outputs:-
    1) top1: The first selected value
    2) top3: The average over three selected values
    3) top5: The average over the first 5 selected values
    """

    topKlist = []

    scoresSorted = -(np.sort(-scoreVec))

    for scoreIdx, scoreItem in enumerate(scoresSorted):
        for eerIdx, eerItem in enumerate(eerVec):
            if(scoreVec[eerIdx] == scoreItem):
                topKlist.append(eerItem)

    if(len(topKlist) >= 5):
        return np.round(topKlist[0],4), np.round(np.average(topKlist[0:3]),4), np.round(np.average(topKlist[0:5]),4)
    else:
        return np.round(topKlist[0],4), np.round(np.average(topKlist[0:3]),4)

