import treeplot
from collections import Counter


def loadDataSet(filepath):
    '''
    Returns
    -----------------
    data: 2-D list
        each row is the feature and label of one instance
    featNames: 1-D list
        feature names
    '''
    data = []
    featNames = None
    fr = open(filepath)
    for (i, line) in enumerate(fr.readlines()):
        array = line.strip().split(',')
        if i == 0:
            featNames = array[:-1]
        else:
            data.append(array)
    return data, featNames


def splitData(dataSet, axis, value):
    '''
    Split the dataset based on the given axis and feature value

    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label
    axis: int
        index of which feature to split on
    value: string
        the feature value to split on

    Returns
    ------------------
    subset: 2-D list
        the subset of data by selecting the instances that have the given feature value
        and removing the given feature columns
    '''
    subset = []
    for instance in dataSet:
        if instance[axis] == value:  # if contains the given feature value
            reducedVec = instance[:axis] + instance[axis + 1:]  # remove the given axis
            subset.append(reducedVec)
    return subset


def chooseBestFeature(dataSet):
    '''
    choose best feature to split based on Gini index

    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label

    Returns
    ------------------
    bestFeatId: int
        index of the best feature
    '''
    # TODO
    '''
    chooseBestFeature(dataset)
        for each feature 𝑖 in the dataset
            calculate gini index on dataset
            for each 𝑣𝑎𝑙𝑢𝑒 of the feature
                subset = splitData(dataset, 𝑖, 𝑣𝑎𝑙𝑢𝑒)
                calculate gini index on the subset
            calculate Gain for feature 𝑖
        Find the bestGain and the corresponding feature id
    '''
    data = list(map(list, zip(*dataSet)))  # transpose data
    gidx = gini(data[data.__len__() - 1])
    _size = dataSet.__len__()
    glist=[]
    for i in range(data.__len__() - 1):
        gidx = gini(data[data.__len__() - 1])
        data[i] = Counter(data[i]).keys()
        temp = []
        size = []
        for y in data[i]:
            subset = splitData(dataSet, i, y)
            print(subset, " ", y)
            size.append(subset.__len__())
            gix = list(map(list, zip(*subset)))
            gi = gini(gix[gix.__len__() - 1])
            temp.append(gi)
        # print(temp)
        g = gain(gidx, temp, size, _size)
        glist.append(g)
    print(glist)
    print(glist.index(max(glist)))
    idx = (glist.index(max(glist)))
    return idx

def gini(data):
    lists = Counter(data).values()
    gini = 1
    for i in lists:
        gini = gini - (i / (data.__len__()) * (i / (data.__len__())))
    return gini


def gain(gidx, l1, l2, size):
    sum = 0
    for i in range(l1.__len__()):
        sum = sum + ((l1[i] / size) * l2[i])
    #print(gidx-sum)
    return gidx - sum


def stopCriteria(dataSet):
    '''
    Criteria to stop splitting:
    1) if all the classe labels are the same, then return the class label;
    2) if there are no more features to split, then return the majority label of the subset.

    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label

    Returns
    ------------------
    assignedLabel: string
        if satisfying stop criteria, assignedLabel is the assigned class label;
        else, assignedLabel is None
    '''
    assignedLabel = None
    # TODO
    '''
    stopCriteria(dataset)
        assignedLabel = None
        if all class labels are the same
            assignedLabel = label
        else if no more features to split
            assignedLabel = majority(labels)
    '''
    data = list(map(list, zip(*dataSet)))
    labels = data[data.__len__()-1]
    labels = list(Counter(labels).keys())
    if labels.__len__()==1:
        assignedLabel = labels[0]
    elif(data.__len__()==1):
        m = max(set(labels), key=labels.count)
        assignedLabel = m
    return assignedLabel


def buildTree(dataSet, featNames):
    '''
    Build the decision tree

    Parameters
    -----------------
    dataSet: 2-D list
        [n'_sampels, m'_features + 1]
        the last column is class label

    Returns
    ------------------
        myTree: nested dictionary
    '''
    assignedLabel = stopCriteria(dataSet)
    if assignedLabel:
        return assignedLabel

    bestFeatId = chooseBestFeature(dataSet)
    bestFeatName = featNames[bestFeatId]

    myTree = {bestFeatName: {}}
    subFeatName = featNames[:]
    del (subFeatName[bestFeatId])
    featValues = [d[bestFeatId] for d in dataSet]
    uniqueVals = list(set(featValues))
    for value in uniqueVals:
        myTree[bestFeatName][value] = buildTree(splitData(dataSet, bestFeatId, value), subFeatName)

    return myTree


if __name__ == "__main__":
    data, featNames = loadDataSet('JavaApplicants.csv')
    dtTree = buildTree(data, featNames)
    # print(dtTree)
    treeplot.createPlot(dtTree)
