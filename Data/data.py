import math
import random

# get 336 values from a secant squared function with random noise
windSpeedData = [(1 - math.cos(2 * math.pi * i / 336))*2 + random.uniform(-1,1 ) for i in range(336)] 

# get 336 random values between 0 and 10
tidalData = [5 + random.uniform(-1,1) for i in range(336)]

# get 336 values from a cosine function with random noise
solarData = [abs(math.cos(2 * math.pi * i / 336)) + random.uniform(-0.1, 0.1) for i in range(336)]