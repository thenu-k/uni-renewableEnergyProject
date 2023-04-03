from Model.Models import *
from UI.UI import *
from Data.Data import *
from Data.helperFunctions import *

# Instantiating the component facilities
tidalInstance =  TidalEnergyModel(
    tidalData=tidalData, 
    isCSV=False,
    unitCount = 1,
    efficiency = 0.8,
    bladeDiameter = 0.5,
    mediumDensity = 997.77,
    accelerationDueToGravity=9.81,
    frequencyOfData=1,
    headHeight=2
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

# print(renewableInstance.TidalEnergyModel.testSingleUnitEnergyProduction(velocity=1.15, isDaily=True, isYearly=False))

totalTest  = [windEnergyGeneration[count] + tidalEnergyGeneration[count] for count in range(336)]

compareProd(
    energyProd=tidalEnergyGeneration,
    energyDemand=energyDemandData,
)