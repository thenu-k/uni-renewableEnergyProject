import csv
import numpy as np

with open('heatmapData.csv', newline='') as csvfile:
    r=csv.reader(csvfile, delimiter=',')
    wind_data=np.transpose([i[1:] for i in list(r)[1:]])

average_wind=9.33    
wind_data=average_wind*np.asarray(wind_data, dtype=float)


nmumber_of_turbines=1
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

monthly_energy=[energy_per_month(i) for i in wind_data]

total_energy=[0]
s=0
for i in monthly_energy:
    s+=i
    total_energy+=[s]
    
print(sum(monthly_energy))   


import matplotlib.pyplot as plt

def data_plotting1(a):
    return [(a[0]+a[-1])/2]+a+[(a[0]+a[-1])/2]

def data_plotting2(a):
    return [(a[0]+a[-1])/2]+2*a+[(a[0]+a[-1])/2]

x_axis1=[0]+[i-0.5 for i in range(1,13)]+[12]
x_axis2=[0]+[i-0.5 for i in range(1,25)]+[24]

plt.plot(x_axis1,data_plotting1(monthly_energy))

##plt.plot(x_axis2,data_plotting2(monthly_energy))

plt.plot(range(13), total_energy)

plt.ylim(0)
plt.show()












