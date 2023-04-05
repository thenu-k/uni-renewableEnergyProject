import math
import random
import numpy as np
from scipy.interpolate import *
import csv 

class Data:
    def retrieveSolarData(error:type[float]):
        return [abs(math.cos(2 * math.pi * i / 336)) + random.uniform(-0.1, 0.1) for i in range(365)]
    
    # Retrieve tidal data
    def generateTidalData(error:type[float], valuesRequired:type[int]):
        numValues = valuesRequired
        currentSpeedData = [0 for i in range(numValues)]
        topCurrentSpeed = 1.15
        bottomCurrentSpeed = 0.6
        alternated=False
        for i in range(numValues):
            if not alternated:
                currentSpeedData[i] = topCurrentSpeed + random.uniform(-topCurrentSpeed*error, topCurrentSpeed*error)
            else:
                currentSpeedData[i] = bottomCurrentSpeed+ random.uniform(-bottomCurrentSpeed*error, bottomCurrentSpeed*error)
            alternated = not alternated if i%7==0 else alternated
        return currentSpeedData

    # Retrieve energy demand data
    def generateEnergyDemandData(error:type[float], interpolate:type[bool], valuesRequired:type[int], currentDataSpacing:type[int]):
        numValues = valuesRequired
        xSpacing = currentDataSpacing
        with open('./Data/Files/energyConsumption.csv', 'r') as f:
            y = f.read().split(',')
            y = [float(i) for i in y]
        y = [y[i]*1e12 for i in range(len(y))]
        x = np.array([xSpacing * (1+i) for i in range(12)])
        values =  [interp1d(x, y, fill_value='extrapolate')(i) for i in range(numValues)]
        townTotal = 7.14e11
        offset = townTotal/sum(values)
        values = [offset * values[i] for i in range(len(values))]
        tidalData = [(value + random.uniform(-value*error, value*error)) for value in values]
        return tidalData

    # Retrieve wind speed data
    def generateWindSpeedData(error:type[float], interpolate:type[bool], valuesRequired:type[int], currentDataSpacing:type[int]):
        numValues = valuesRequired
        daysInMonth = currentDataSpacing
        with open('./Data/Files/heatmapData.csv', newline='') as csvfile:
            r=csv.reader(csvfile, delimiter=',')
            windData=np.transpose([i[1:] for i in list(r)[1:]])
        average_wind=9.33    
        windData=(average_wind*np.asarray(windData, dtype=float))
        windData = [sum(windData[count])/len(windData[count]) for count in range(len(windData))]
        xValues = np.array([daysInMonth * (1+i) for i in range(12)])
        values =  [interp1d(xValues, windData, fill_value='extrapolate')(i) for i in range(numValues)]
        y_values = [(value + random.uniform(-value*error, value*error)) for value in values]
        return y_values