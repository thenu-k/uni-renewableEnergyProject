from Model.Models import *
from UI.UI import *
from Data.Data import *

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