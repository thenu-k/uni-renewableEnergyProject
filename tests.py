from Model.RenewableEnergyModel import RenewableEnergyModel
from Model.ComponentModels.EnergyStorageModel import EnergyStorageModel
from Model.ComponentModels.TidalEnergyModel import TidalEnergyModel
from Model.ComponentModels.WindEnergyModel import WindEnergyModel
from Model.ComponentModels.SolarEnergyModel import SolarEnergyModel
from UI.UI import *
from Data.Data import Data
import matplotlib as mpl
formatter = mpl.ticker.EngFormatter()

numDataPoints = 365
error = 0.025

# Instantiating the component facilities
tidalInstance =  TidalEnergyModel(
    tidalData=Data.generateTidalData(
        error=error,
        valuesRequired=numDataPoints,
    ), 
    unitCount = 5,
    efficiency = 0.87,
    bladeDiameter = 0.81,
    mediumDensity = 997.77,
    accelerationDueToGravity=9.81,
    headHeight=20,
    isCrossFlow=True,
    customPower=None,
)
windInstance = WindEnergyModel(
    windData=Data.generateWindSpeedData(
        error=error,
        interpolate=True,
        valuesRequired = numDataPoints,
        currentDataSpacing=30,
    ),
    unitCount=20,
    efficiency=0.4,
    bladeDiameter=174,
    mediumDensity=1.225,
    customDailyGenerationFunction=None,
)
solarInstance = SolarEnergyModel(
    solarData=Data.retrieveSolarData(error=0),
    customPower=450,
    unitCount=5e2,
)
storageInstance = EnergyStorageModel(
    liquidDensity=1000,
    accelerationDueToGravity=9.81,
    maxFlowRate=100,
    efficiency=1,
    maxTopVolume=3e100,
    currentTopVolume=1.5e50,
    maxBottomValue=5e100,
    currentBottomValue=4.5e50,
    heightDifference=250,
    turbinePower=1e5*100,
    minimumWaterLevel=0,
    dataValues=numDataPoints
)
# Connecting the facilities together
energyDemandData = Data.generateEnergyDemandData(
        error=error,
        interpolate=True,
        valuesRequired=numDataPoints,
        currentDataSpacing=30
)
renewableInstance = RenewableEnergyModel(
    TidalEnergyModel=tidalInstance,
    WindEnergyModel=windInstance,
    SolarEnergyModel=solarInstance,
    EnergyStorageModel=storageInstance,
    dataValues=numDataPoints,
    energyDemand=energyDemandData
)
tidalEnergyGeneration = renewableInstance.TidalEnergyModel.getDailyEnergyProduction()
windEnergyGeneration = renewableInstance.WindEnergyModel.getDailyEnergyProduction()
solarEnergyGeneration = renewableInstance.SolarEnergyModel.getDailyEnergyProduction()
totalEnergyGeneration = renewableInstance.getDailyTotalEnergyProduction()
netEnergyDemand = renewableInstance.getNetDailyEnergyDemand()
[excessEnergy, energyMovementValues] = renewableInstance.accountForEnergyStorage()

print(energyMovementValues[0])

compareProd(
    graphs=[
        # tidalEnergyGeneration,
        # windEnergyGeneration,
        # totalEnergyGeneration,
        energyDemandData,
        # netEnergyDemand,
        # excessEnergy,
    
    ]
)