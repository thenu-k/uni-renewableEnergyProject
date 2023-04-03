from Model.Models import *
from UI.UI import *
from Data.Data import *
from Data.helperFunctions import *

# Instantiating the component facilities
tidalInstance =  TidalEnergyModel(
    tidalData=tidalData, 
    isCSV=False,
    unitCount = 10,
    efficiency = 0.8,
    bladeDiameter = 5,
    mediumDensity = 997.77,
    accelerationDueToGravity=9.81,
    headHeight=20,
    frequencyOfData=1,
)
windInstance = WindEnergyModel(
    windData=None,
    customDailyGenerationFunction=generateWindSpeedData,
    isCSV=False,
    frequencyOfData=None,
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
    dataValues=len(tidalData)
)
# Connecting the facilities together
renewableInstance = RenewableEnergyModel(tidalInstance, windInstance, solarInstance, storageInstance)
tidalEnergyGeneration = renewableInstance.TidalEnergyModel.getDailyEnergyProduction()
windEnergyGeneration = renewableInstance.WindEnergyModel.getDailyEnergyProduction()
solarEnergyGeneration = renewableInstance.SolarEnergyModel.getDailyEnergyProduction()
totalEnergyGeneration = renewableInstance.getDailyTotalEnergyProduction()
netEnergyDemand = renewableInstance.getNetDailyEnergyDemand(
    energyDemand=energyDemandData, frequencyOfData=1,
)

# Plotting the data
plotData(
    tidalEnergyGeneration=tidalEnergyGeneration,
    windEnergyGeneration=windEnergyGeneration,
    solarEnergyGeneration=solarEnergyGeneration,
    totalEnergyGeneration=totalEnergyGeneration,
    netEnergyDemand=netEnergyDemand,
)
