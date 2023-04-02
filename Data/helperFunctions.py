import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import random

'''
    Generate Energy Demand Data ======================================
    The raw energy demand data has data for the entirety of the UK and is only monthly.
    This function interpolates the data to get a value for every day, assuming a month has 28 days.
    An error of up to 5% is added to each value using a uniform distribution.
'''
def interpolateEnergyData():
    with open('./Data/Files/energyConsumption.csv', 'r') as f:
        y = f.read().split(',')
        y = [float(i) for i in y]
    y = [y[i]*1e12 for i in range(len(y))]
    x = np.array([28 * (1+i) for i in range(12)])
    values =  [interp1d(x, y, fill_value='extrapolate')(i) for i in range(336)]
    townTotal = 7.14e11
    offset = townTotal/sum(values)
    values = [offset * values[i] for i in range(len(values))]
    x_values = np.linspace(0, 336, num=336)
    y_values = [(value + random.uniform(-value*0.05, value*0.05)) for value in values]
    with open('./Data/Files/energyDemand.csv', 'w') as f:
        for item in y_values:
            if item == y_values[-1]:
                f.write("%s" % item)
            else:
                f.write("%s," % item)
    plt.plot(x_values, y_values)
    plt.show()
'''
    Generate Current Speed Data ======================================
    Sea current speeds alternate between 1.15 m/s and 0.6 m/s every week.
    An error is then added to each value using a uniform distribution.
'''
def generateCurrentData():
    currentSpeedData = [0]*336
    for i in range(int(336/7)):
        if i % 2 == 0:
            # add random error to the current speed
            currentSpeedData[i*7:i*7+7] = [1.15 + random.uniform(-0.1, 0.1) for i in range(7)]
        else:
            currentSpeedData[i*7:i*7+7] = [0.6+ random.uniform(-0.1, 0.1) for i in range(7)]
    x_values = np.linspace(0, 336, num=336)
    y_values = [currentSpeedData for currentSpeedData in currentSpeedData]
    with open('./Data/Files/currentSpeed.csv', 'w') as f:
        for item in y_values:
            # remove comman from last item
            if item == y_values[-1]:
                f.write("%s" % item)
            else:
                f.write("%s," % item)
    plt.plot(x_values, y_values)
    plt.show()
'''
    Generate Wind Speed Data ======================================
'''
def generateWindSpeedData():
    return [10 for i in range(336)]