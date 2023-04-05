import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import random
import csv
from Model.helperFunctions import *

'''
    Generate Energy Demand Data ======================================
    The raw energy demand data has data for the entirety of the UK and is only monthly.
    This function interpolates the data to get a value for every day, assuming a month has 28 days.
    An error of up to 5% is added to each value using a uniform distribution.
'''
def generateEnergyDemandData(error:type[float], interpolate:type[bool], valuesRequired:type[int], currentDataSpacing:type[int]):
    numValues = 365
    xSpacing = 30
    with open('./Data/Files/energyConsumption.csv', 'r') as f:
        y = f.read().split(',')
        y = [float(i) for i in y]
    y = [y[i]*1e12 for i in range(len(y))]
    x = np.array([xSpacing * (1+i) for i in range(12)])
    values =  [interp1d(x, y, fill_value='extrapolate')(i) for i in range(numValues)]
    townTotal = 7.14e11
    offset = townTotal/sum(values)
    values = [offset * values[i] for i in range(len(values))]
    y_values = [(value + random.uniform(-value*error, value*error)) for value in values]
    return y_values


'''
    Generate Current Speed Data ======================================
    Sea current speeds alternate between 1.15 m/s and 0.6 m/s every week.
    An error is then added to each value using a uniform distribution.
'''
def generateCurrentData(error:type[float]):
    numValues = 365
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


'''
    Generate Wind Speed Data ======================================
'''
def generateWindSpeedData(error=0.005):
    numValues = 365
    daysInMonth = 30
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


'''
    Custom Wind Energy Generation Function ======================================
'''
def generateWindEnergyData():
    with open('Data/Files/heatmapData.csv', newline='') as csvfile:
        r=csv.reader(csvfile, delimiter=',')
        wind_data=np.transpose([i[1:] for i in list(r)[1:]])

    average_wind=9.33    
    wind_data=average_wind*np.asarray(wind_data, dtype=float)


    nmumber_of_turbines=10
    efficiency_factor=0.4
    diameter=174
    air_density=1.225

    def energy_per_hour(v):
        ##in kWh
        return nmumber_of_turbines*efficiency_factor*air_density*v**3/2*np.pi*diameter**2/4000

    def energy_per_month(month):
        ##in GWh
        sum=0
        for v in month:
            sum+=energy_per_hour(v)        
        return sum*30/10**6

    def energy_per_year(year):
        ##in GWh
        sum=0
        for month in year:
            sum+=energy_per_month(month)
        return sum

    monthly_energy=[energy_per_month(i)*1e9/30 for i in wind_data] #in GWh for the entire month so *1e9/30
    x = np.array([28 * (1+i) for i in range(12)])
    y= monthly_energy
    normalizedData = [interp1d(x, y, fill_value='extrapolate')(i) for i in range(336)]
    normalizedData = [normalizedDataValue + random.uniform(-normalizedDataValue*0.05, normalizedDataValue*0.05) for normalizedDataValue in normalizedData]
    # plt.plot([count for count in range(12)], monthly_energy)
    # plt.show()
    # print(sum(normalizedData))
    return normalizedData


'''
    Create a CSV file of the data ======================================
'''
def generateCSVFile(data, fileName):
    with open(fileName, 'w') as f:
        count = 0
        for item in data:
            # remove comman from last item
            if count == len(data)-1:
                f.write("%s" % item)
            else:
                f.write("%s," % item)
            count += 1
