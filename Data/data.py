import math
import random
import numpy as np
from scipy.interpolate import *
import matplotlib.pyplot as plt

# get 336 values from a secant squared function with random noise
windSpeedData = [(1 - math.cos(2 * math.pi * i / 336))*2 + random.uniform(-1,1 ) for i in range(336)] 

# get 336 random values between 0 and 10
with open('./Data/Files/currentSpeed.csv', 'r') as f:
        tidalData = f.read().split(',')
        tidalData = [float(i) for i in tidalData]

# get 336 values from a cosine function with random noise
solarData = [abs(math.cos(2 * math.pi * i / 336)) + random.uniform(-0.1, 0.1) for i in range(336)]

# get 336 values from a secant squared function with random noise
with open('./Data/Files/energyDemand.csv', 'r') as f:
        energyDemandData = f.read().split(',')
        energyDemandData = [float(i) for i in energyDemandData]

# Wind speed data
with open('./Data/Files/windSpeed.csv', 'r') as f:
        windSpeedData = f.read().split(',')
        windSpeedData = [float(i) for i in windSpeedData]