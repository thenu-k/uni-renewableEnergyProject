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
    currentSpeedData = [0 for i in range(336)]
    for i in range(int(336/7)):
        if i % 2 == 0:
            # add random error to the current speed
            currentSpeedData[i*7:i*7+7] = [1.15 + random.uniform(-0.1, 0.1) for i in range(7)]
        else:
            currentSpeedData[i*7:i*7+7] = [0.6+ random.uniform(-0.1, 0.1) for i in range(7)]
    x_values = np.linspace(0, 336, num=336)
    with open('./Data/Files/currentSpeedConstant.csv', 'w') as f:
        count = 0
        for item in currentSpeedData:
            # remove comman from last item
            if count == len(currentSpeedData)-1:
                f.write("%s" % item)
            else:
                f.write("%s," % item)
            count += 1
    plt.plot(x_values, currentSpeedData)
    plt.show()
'''
    Generate Wind Speed Data ======================================
'''
def generateWindSpeedData():
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