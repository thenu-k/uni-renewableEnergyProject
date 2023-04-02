'''
    This function will help normalize the data set. It takes in a dataset, and how often the data needs 
    to be repeated.
    For example if the dataset contains the 12 values and the frequency is 28, each value will be repeated 28 times.
'''

def normalizeDataSet(dataset, frequency):
    normalizedData = [0] * 28 * 12
    count = 0
    for i in range(len(dataset)):
        for j in range(frequency):
            normalizedData[count] = dataset[i]
            count += 1
    return normalizedData

def langrangianInterpolator(dataset, currFrequency, requiredFrequency, numValues):
    pass