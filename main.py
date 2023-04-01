from Model.Models import *
from UI.UI import *
from Data.data import *

# Instantiating the component facilities
tidalInstance =  TidalEnergyModel(
    tidalData=tidalData, 
    isCSV=False,
    frequencyOfData=1,
    )
windInstance = WindEnergyModel(
    windData=windSpeedData, 
    isCSV=False,
    frequencyOfData=1,
)
solarInstance = SolarEnergyModel(
    solarData=solarData, 
    isCSV=False,
    frequencyOfData=1,
)
storageInstance = EnergyStorage(
    liquidDensity=1000,
    accelerationDueToGravity=9.81,
    maxFlowRate=100,
    efficiency=0.5,
    maxTopVolume=100,
    maxBottomValue=100,
    turbinePower=100,
)

# Connecting the facilities together
renewableInstance = RenewableEnergyModel(tidalInstance, windInstance, solarInstance, storageInstance)
tidalEnergyGeneration = tidalInstance.getTidalEnergyGeneration()
windEnergyGeneration = windInstance.getWindGeneration()
solarEnergyGeneration = solarInstance.getSolarGeneration()
totalEnergyGeneration = renewableInstance.getPowerGeneration()

# Plotting the data
plotData(
    tidalEnergyGeneration=tidalEnergyGeneration,
    windEnergyGeneration=windEnergyGeneration,
    solarEnergyGeneration=solarEnergyGeneration,
    totalEnergyGeneration=totalEnergyGeneration,
)